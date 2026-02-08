"""
=============================================================================
  Prepy.ai - AI-Powered Mock Interview Preparation Tool
=============================================================================
  Main Streamlit application file.

  HOW THE APP WORKS:
  ─────────────────
  The app has THREE main views, controlled by session_state:
    1. HOME PAGE    - Landing page with description, features, team, etc.
                       Shown when page == "home"
    2. INTERVIEW    - Setup sidebar + interview chat interface.
                       Shown when page == "interview"
       a) SETUP VIEW  - Hero card with steps, material preview
                         (when interview hasn't started yet)
       b) CHAT VIEW   - Live interview with AI interviewer
                         (when interview is in progress)
       c) FEEDBACK    - Performance report after stopping interview
    3. Navigation is handled by session_state["page"]

  KEY FILES:
  ──────────
  app.py                          ← YOU ARE HERE (main UI + logic)
  styles.py                       ← All CSS, HTML templates, home page HTML
  backend/
    pdf_reader.py                 ← Extracts text from uploaded PDF resumes
    models/
      gemini_model.py             ← Google Gemini AI: generates questions & feedback
      audio_tts.py                ← ElevenLabs: converts interviewer text to speech
    prompts/
      interviewer.txt             ← System prompt that defines interviewer behavior
      evaluation.txt              ← System prompt for generating feedback

  SESSION STATE KEYS (what each one stores):
  ──────────────────
  page                → Current page: "home" or "interview"
  conversation        → List of dicts: [{"interviewer": "...", "candidate": "..."}]
  started             → bool: whether an interview is currently in progress
  job_description     → str: the pasted job description text
  resume_text         → str: extracted text from the uploaded PDF
  resume_pdf_bytes    → bytes: raw PDF for rendering/download
  feedback            → str or None: AI-generated feedback after interview ends
  last_tts_audio      → bytes or None: most recent TTS audio to play
  tts_played_for_turn → int: tracks which turn's TTS has been played (avoids replays)
  processed_audio_hash→ str or None: MD5 hash of last processed voice recording
  interviewer_name    → str: configurable name for the AI interviewer
  pending_transcription → str or None: transcribed text waiting to be sent
  show_material       → str or None: "resume" or "jd" toggle for viewing materials
  auto_send_voice     → bool: whether to auto-send after voice transcription
  interview_session_id→ int: unique ID per session (used for input key uniqueness)
=============================================================================
"""

# ─── IMPORTS ────────────────────────────────────────────────────────────────
import streamlit as st
import streamlit.components.v1 as components
import hashlib
import os
import tempfile
import torch
import soundfile as sf
import librosa
import pypdfium2 as pdfium
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Backend modules
from backend.models.gemini_model import interview_response, interview_feedback
from backend.pdf_reader import extract_text_from_pdf
from backend.models.audio_tts import speak_text

# Styling: CSS templates, HTML snippets, and home page content
from styles import (
    GLOBAL_CSS,
    CHAT_HTML_TEMPLATE,
    HERO_HTML,
    SIDEBAR_HEADER_HTML,
    HOME_PAGE_HTML,
)


# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
# Must be the first Streamlit command. Sets browser tab title, icon, and layout.
st.set_page_config(
    page_title="Prepy.ai - Mock Interview Prep",
    page_icon="🎯",
    layout="wide"
)

# Inject global CSS (fonts, sidebar styling, buttons, inputs, etc.)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─── SESSION STATE INITIALIZATION ───────────────────────────────────────────
# Each key is initialized only once per session. This block runs on every
# Streamlit rerun but only sets defaults if the key doesn't exist yet.

if "page" not in st.session_state:
    st.session_state.page = "home"                  # Start on home page

if "conversation" not in st.session_state:
    st.session_state.conversation = []              # Interview Q&A history

if "started" not in st.session_state:
    st.session_state.started = False                # Is interview in progress?

if "job_description" not in st.session_state:
    st.session_state.job_description = ""           # Pasted JD text

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""               # Extracted resume text

if "resume_pdf_bytes" not in st.session_state:
    st.session_state.resume_pdf_bytes = None        # Raw PDF bytes for rendering

if "feedback" not in st.session_state:
    st.session_state.feedback = None                # AI feedback after interview

if "last_tts_audio" not in st.session_state:
    st.session_state.last_tts_audio = None          # Latest TTS audio bytes

if "tts_played_for_turn" not in st.session_state:
    st.session_state.tts_played_for_turn = -1       # Which turn's audio was played

if "processed_audio_hash" not in st.session_state:
    st.session_state.processed_audio_hash = None    # MD5 of last processed recording

if "interviewer_name" not in st.session_state:
    st.session_state.interviewer_name = "Stacy"     # Default interviewer name

if "pending_transcription" not in st.session_state:
    st.session_state.pending_transcription = None   # Transcribed text awaiting send

if "show_material" not in st.session_state:
    st.session_state.show_material = None           # Which material to show: "resume"/"jd"

if "auto_send_voice" not in st.session_state:
    st.session_state.auto_send_voice = False        # Auto-send after transcription?

if "interview_session_id" not in st.session_state:
    st.session_state.interview_session_id = 0       # Unique ID for input key cycling


# ─── HELPER FUNCTIONS ──────────────────────────────────────────────────────

def render_pdf_as_images(pdf_bytes, max_pages=5):
    """
    Renders PDF pages as images in the Streamlit UI.
    Uses pypdfium2 instead of an iframe (which is blocked in Streamlit's sandbox).
    Falls back to a download button if rendering fails.
    """
    try:
        pdf = pdfium.PdfDocument(pdf_bytes)
        total = len(pdf)
        pages_to_show = min(total, max_pages)
        for i in range(pages_to_show):
            page = pdf[i]
            bitmap = page.render(scale=1.5)
            pil_image = bitmap.to_pil()
            st.image(pil_image, use_container_width=True)
        if total > max_pages:
            st.caption(f"Showing first {max_pages} of {total} pages. Download the PDF to view all.")
        pdf.close()
    except Exception:
        st.warning("Could not render PDF preview. You can download it instead.")
        st.download_button(
            "Download Resume PDF",
            data=pdf_bytes,
            file_name="resume.pdf",
            mime="application/pdf",
            key="pdf_fallback"
        )


def _escape_html(text):
    """Escapes HTML special characters to prevent XSS in chat bubbles."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def render_chat(conversation, interviewer_name):
    """
    Renders the interview conversation as styled chat bubbles.

    Uses components.html() to inject a full HTML document into an iframe,
    which gives us proper CSS isolation (flexbox, gradients, etc.) that
    st.markdown can't reliably provide.

    Each interviewer message gets a question number badge (Q1, Q2...).
    Auto-scrolls to the bottom after rendering.
    """
    bubbles_html = ""
    q_num = 0
    interviewer_initial = interviewer_name[0].upper() if interviewer_name else "I"

    for turn in conversation:
        q_num += 1

        # ── Interviewer bubble (left-aligned, gray gradient) ──
        interviewer_msg = _escape_html(turn['interviewer']).replace('\n', '<br>')
        bubbles_html += f"""
        <div class="chat-bubble chat-bubble-left">
            <div class="chat-meta">
                <div class="chat-avatar avatar-interviewer">{_escape_html(interviewer_initial)}</div>
                <div class="chat-name">{_escape_html(interviewer_name)}</div>
                <span class="q-number">Q{q_num}</span>
            </div>
            {interviewer_msg}
        </div>
        """

        # ── Candidate bubble (right-aligned, indigo gradient) ──
        if turn["candidate"]:
            candidate_msg = _escape_html(turn['candidate']).replace('\n', '<br>')
            bubbles_html += f"""
            <div class="chat-bubble chat-bubble-right">
                <div class="chat-meta">
                    <div class="chat-avatar avatar-user">Y</div>
                    <div class="chat-name">You</div>
                </div>
                {candidate_msg}
            </div>
            """

    # Estimate iframe height based on number of bubbles
    bubble_count = sum(1 + (1 if t["candidate"] else 0) for t in conversation)
    estimated_height = max(250, bubble_count * 140)

    # Inject bubbles into the chat HTML template (defined in styles.py)
    full_html = CHAT_HTML_TEMPLATE.format(bubbles=bubbles_html)
    components.html(full_html, height=estimated_height, scrolling=True)


@st.cache_resource
def load_whisper():
    """
    Loads the Whisper speech-to-text model (small variant).
    Cached with @st.cache_resource so it only downloads/loads once per session.
    Returns the processor (tokenizer) and the model.
    """
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    model.config.forced_decoder_ids = None
    return processor, model


def send_answer(answer_text):
    """
    Sends the candidate's answer to the AI interviewer and gets the next question.

    Steps:
      1. Saves the answer into the current conversation turn
      2. Calls Gemini to generate the next interviewer question
      3. Generates TTS audio for the new question
      4. Appends a new conversation turn for the next question
      5. Reruns Streamlit to update the UI
    """
    iname = st.session_state.interviewer_name

    if not st.session_state.conversation:
        st.warning("No interview in progress.")
        return

    # Save the candidate's answer to the current (last) turn
    st.session_state.conversation[-1]["candidate"] = answer_text

    # Get the next question from Gemini AI
    next_resp = interview_response(
        st.session_state.job_description,
        st.session_state.resume_text,
        st.session_state.conversation,
        answer_text,
        interviewer_name=iname
    )

    # Generate text-to-speech audio for the new question
    try:
        tts_bytes = speak_text(next_resp)
        st.session_state.last_tts_audio = tts_bytes
    except Exception:
        st.session_state.last_tts_audio = None

    # Add a new turn for the next question (candidate answer is empty until they respond)
    st.session_state.conversation.append({
        "interviewer": next_resp,
        "candidate": ""
    })

    # Reset transcription and audio state for the next turn
    st.session_state.pending_transcription = None
    st.session_state.processed_audio_hash = None
    st.session_state.tts_played_for_turn = -1
    st.rerun()


# =============================================================================
#  PAGE ROUTING - Decides which page to show based on session_state["page"]
# =============================================================================

if st.session_state.page == "home":
    # ─────────────────────────────────────────────────────────────────────────
    #  HOME PAGE
    #  Shows: description, demo video placeholder, features, team, future
    #  improvements, and a "Start Practicing" button to go to interview page
    # ─────────────────────────────────────────────────────────────────────────

    # Bold, prominent "Start Practicing Now" button at the TOP
    st.markdown("""
    <style>
    div[data-testid="stButton"] > button[kind="secondary"][key*="goto_interview"],
    .bold-start-btn > div > button {
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        border: none !important;
        border-radius: 12px !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 14px rgba(79,70,229,0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_top1, col_top2, col_top3 = st.columns([1, 2, 1])
    with col_top2:
        if st.button("Start Practicing Now", use_container_width=True, key="goto_interview_top", type="primary"):
            st.session_state.page = "interview"
            st.rerun()

    # Render the full home page HTML (hero, features, video, team, etc.)
    components.html(
        f"""<html><head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        </head><body style="margin:0;padding:0;font-family:'Inter',sans-serif;overflow:hidden;">
        {HOME_PAGE_HTML}
        </body></html>""",
        height=3000,
        scrolling=False
    )

    # Bold "Start Practicing Now" button at the BOTTOM too
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Practicing Now", use_container_width=True, key="goto_interview", type="primary"):
            st.session_state.page = "interview"
            st.rerun()

    # Footer
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #94A3B8;
        font-size: 0.8rem;
        font-family: 'Inter', sans-serif;
        border-top: 1px solid #E2E8F0;
        margin-top: 2rem;
    ">
        Made with ❤️ by the Prepy.ai team &nbsp;|&nbsp; Powered by Google Gemini & ElevenLabs
    </div>
    """, unsafe_allow_html=True)


elif st.session_state.page == "interview":
    # ─────────────────────────────────────────────────────────────────────────
    #  INTERVIEW PAGE
    #  Contains: sidebar (config, controls), and the main interview area
    # ─────────────────────────────────────────────────────────────────────────

    # ── Page title ──
    st.title("Prepy.ai")

    # ── SIDEBAR: Branding + Configuration ────────────────────────────────────
    # The sidebar has: app logo, interviewer name, job description input,
    # resume upload, start button, and stop/feedback button.

    st.sidebar.markdown(SIDEBAR_HEADER_HTML, unsafe_allow_html=True)

    # "Back to Home" link in sidebar
    if st.sidebar.button("← Back to Home", use_container_width=True, key="back_home"):
        st.session_state.page = "home"
        st.rerun()

    st.sidebar.markdown("---")

    # Section label: Configuration
    st.sidebar.markdown(
        "<p style='color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; "
        "letter-spacing: 0.08em; font-weight: 600; margin-bottom: 0.5rem; "
        "font-family: Inter, sans-serif;'>Configuration</p>",
        unsafe_allow_html=True
    )

    # Interviewer name input (default: "Stacy", passed to Gemini prompt)
    interviewer_name = st.sidebar.text_input(
        "Interviewer Name",
        value=st.session_state.interviewer_name
    )
    st.session_state.interviewer_name = interviewer_name

    # Job description text area
    job_description_text = st.sidebar.text_area(
        "Job Description (paste text)",
        value=st.session_state.job_description
    )

    # Resume PDF uploader
    resume_pdf = st.sidebar.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    # ── Process uploaded resume ──
    # Extract text from PDF using pdfplumber; store both text and raw bytes
    resume_text = st.session_state.resume_text

    if resume_pdf:
        resume_text = extract_text_from_pdf(resume_pdf)
        st.session_state.resume_pdf_bytes = resume_pdf.getvalue()
        if resume_text:
            st.session_state.resume_text = resume_text
            st.sidebar.success("Resume uploaded successfully.")
        else:
            st.session_state.resume_text = ""
            st.sidebar.error("Could not read text from this PDF. Please try a different file.")

    st.sidebar.markdown("")

    # ── START INTERVIEW BUTTON ───────────────────────────────────────────────
    # Validates inputs, resets session, calls Gemini for the first question,
    # generates TTS, and starts the interview.
    if st.sidebar.button("🚀  Start Interview", use_container_width=True):
        if not job_description_text or not resume_text:
            st.warning("Please provide BOTH a job description and a resume.")
        else:
            try:
                # Reset all interview-related state
                st.session_state.started = True
                st.session_state.conversation = []
                st.session_state.feedback = None
                st.session_state.last_tts_audio = None
                st.session_state.tts_played_for_turn = -1
                st.session_state.processed_audio_hash = None
                st.session_state.pending_transcription = None
                st.session_state.show_material = None
                st.session_state.interview_session_id = id(st.session_state)
                st.session_state.job_description = job_description_text

                # Get the first interview question from Gemini
                first_question = interview_response(
                    job_description_text,
                    resume_text,
                    [],  # Empty conversation history for the first question
                    "Start the interview.",
                    interviewer_name=st.session_state.interviewer_name
                )

                # Generate TTS audio for the first question
                try:
                    tts_bytes = speak_text(first_question)
                    st.session_state.last_tts_audio = tts_bytes
                except Exception:
                    st.session_state.last_tts_audio = None

                # Add the first turn to conversation history
                st.session_state.conversation.append({
                    "interviewer": first_question,
                    "candidate": ""
                })
                st.rerun()
            except ValueError as e:
                st.error(str(e))
                st.session_state.started = False

    st.sidebar.markdown("---")

    # Section label: Session
    st.sidebar.markdown(
        "<p style='color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; "
        "letter-spacing: 0.08em; font-weight: 600; margin-bottom: 0.5rem; "
        "font-family: Inter, sans-serif;'>Session</p>",
        unsafe_allow_html=True
    )

    # ── STOP & GET FEEDBACK BUTTON ───────────────────────────────────────────
    # Sends the full conversation to Gemini's evaluation prompt and displays
    # a detailed performance report.
    if st.sidebar.button("🛑  Stop & Get Feedback", use_container_width=True):
        if st.session_state.conversation:
            try:
                with st.spinner("Generating your feedback report..."):
                    feedback_text = interview_feedback(
                        st.session_state.job_description,
                        st.session_state.resume_text,
                        st.session_state.conversation,
                    )
                st.session_state.feedback = feedback_text
                st.session_state.started = False
                st.session_state.last_tts_audio = None
                st.session_state.show_material = None
                st.rerun()
            except ValueError as e:
                st.error(str(e))
        else:
            st.sidebar.warning("No interview in progress.")


    # =========================================================================
    #  MAIN CONTENT AREA - Three possible views:
    #    1. Setup view (not started, no feedback)
    #    2. Feedback view (interview ended)
    #    3. Interview chat view (interview in progress)
    # =========================================================================

    if not st.session_state.started and not st.session_state.feedback:
        # ── SETUP VIEW ──────────────────────────────────────────────────────
        # Shown before the interview starts. Displays a hero card with
        # instructions and lets users preview their uploaded materials.

        st.markdown(HERO_HTML, unsafe_allow_html=True)

        # Material preview radio buttons (only shown if materials exist)
        if st.session_state.resume_pdf_bytes or job_description_text:
            view_option = st.radio(
                "Preview your materials",
                options=["Resume", "Job Description", "Side by Side"],
                horizontal=True
            )

            if view_option == "Resume":
                if st.session_state.resume_pdf_bytes:
                    st.subheader("Your Resume")
                    st.download_button(
                        "Download PDF",
                        data=st.session_state.resume_pdf_bytes,
                        file_name="resume.pdf",
                        mime="application/pdf"
                    )
                    render_pdf_as_images(st.session_state.resume_pdf_bytes)
                else:
                    st.info("Upload a resume PDF in the sidebar to preview it here.")
            elif view_option == "Job Description":
                if job_description_text:
                    st.subheader("Job Description")
                    st.write(job_description_text)
                else:
                    st.info("Paste a job description in the sidebar to preview it here.")
            else:
                # Side by side view
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Your Resume")
                    if st.session_state.resume_pdf_bytes:
                        st.download_button(
                            "Download PDF",
                            data=st.session_state.resume_pdf_bytes,
                            file_name="resume.pdf",
                            mime="application/pdf",
                            key="dl_side"
                        )
                        render_pdf_as_images(st.session_state.resume_pdf_bytes)
                    else:
                        st.info("Upload a resume PDF in the sidebar.")
                with col2:
                    st.subheader("Job Description")
                    if job_description_text:
                        st.write(job_description_text)
                    else:
                        st.info("Paste a job description in the sidebar.")


    elif st.session_state.feedback:
        # ── FEEDBACK VIEW ───────────────────────────────────────────────────
        # Shown after the interview is stopped. Displays the AI's performance
        # report with a styled header card.

        feedback_text = st.session_state.feedback

        # Styled report card header
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(6,182,212,0.08) 100%);
            border: 1px solid rgba(16,185,129,0.15);
            border-radius: 16px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
            text-align: center;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <h2 style="
                font-family: 'Inter', sans-serif;
                font-weight: 800;
                font-size: 1.4rem;
                color: #1E293B;
                margin: 0;
                letter-spacing: -0.02em;
            ">Interview Performance Report</h2>
            <p style="
                font-family: 'Inter', sans-serif;
                color: #64748B;
                font-size: 0.9rem;
                margin: 0.3rem 0 0 0;
            ">Here's your detailed feedback from the mock interview session</p>
        </div>
        """, unsafe_allow_html=True)

        # Render the actual feedback (Gemini returns markdown)
        st.markdown(feedback_text)

        # Action buttons: start a new interview or go back home
        st.markdown("")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄  Start New Interview", use_container_width=True):
                st.session_state.feedback = None
                st.session_state.conversation = []
                st.session_state.started = False
                st.rerun()
        with col2:
            if st.button("🏠  Back to Home", use_container_width=True, key="feedback_home"):
                st.session_state.feedback = None
                st.session_state.conversation = []
                st.session_state.started = False
                st.session_state.page = "home"
                st.rerun()


    elif st.session_state.started:
        # ── INTERVIEW CHAT VIEW ─────────────────────────────────────────────
        # The main interview interface. Shows:
        #   - Progress header (question count, answers given)
        #   - Material toggle buttons (resume/JD)
        #   - TTS audio player (auto-plays new questions)
        #   - Chat bubbles (interviewer + candidate)
        #   - Answer input area (type or voice)

        iname = st.session_state.interviewer_name
        num_questions = len(st.session_state.conversation)
        num_answered = sum(1 for t in st.session_state.conversation if t["candidate"])

        # ── Progress header bar ──
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: linear-gradient(135deg, rgba(79,70,229,0.06) 0%, rgba(6,182,212,0.06) 100%);
            border: 1px solid rgba(79,70,229,0.1);
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 1rem;
            font-family: 'Inter', sans-serif;
        ">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.2rem;">🎤</span>
                <span style="font-weight: 600; color: #1E293B; font-size: 0.95rem;">
                    Interview with {_escape_html(iname)}
                </span>
            </div>
            <div style="display: flex; gap: 16px; align-items: center;">
                <span style="
                    background: rgba(79,70,229,0.1);
                    color: #4F46E5;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 600;
                ">Q{num_questions}</span>
                <span style="
                    background: rgba(16,185,129,0.1);
                    color: #059669;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 600;
                ">{num_answered} answered</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Material toggle buttons (Resume / Job Description) ──
        # Clicking toggles visibility of the material on the main screen
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 3])
        with btn_col1:
            if st.button("📄 Resume", use_container_width=True):
                st.session_state.show_material = (
                    "resume" if st.session_state.show_material != "resume" else None
                )
                st.rerun()
        with btn_col2:
            if st.button("📋 JD", use_container_width=True):
                st.session_state.show_material = (
                    "jd" if st.session_state.show_material != "jd" else None
                )
                st.rerun()

        # ── Expandable material panels ──
        if st.session_state.show_material == "resume" and st.session_state.resume_pdf_bytes:
            with st.expander("Resume", expanded=True):
                st.download_button(
                    "Download PDF",
                    data=st.session_state.resume_pdf_bytes,
                    file_name="resume.pdf",
                    mime="application/pdf",
                    key="dl_interview"
                )
                render_pdf_as_images(st.session_state.resume_pdf_bytes)
        elif st.session_state.show_material == "jd" and st.session_state.job_description:
            with st.expander("Job Description", expanded=True):
                st.write(st.session_state.job_description)

        # ── TTS Audio Player ──
        # Plays the interviewer's voice for the latest question.
        # Only plays once per turn (tracked by tts_played_for_turn).
        current_turn = len(st.session_state.conversation) - 1
        if st.session_state.last_tts_audio and st.session_state.tts_played_for_turn != current_turn:
            st.audio(st.session_state.last_tts_audio, format="audio/mp3", autoplay=True)
            st.session_state.tts_played_for_turn = current_turn

        # ── Chat Bubbles ──
        render_chat(st.session_state.conversation, iname)

        # ── Visual separator ──
        st.markdown("""
        <div style="
            height: 1px;
            background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
            margin: 1rem 0;
        "></div>
        """, unsafe_allow_html=True)

        # ── ANSWER INPUT AREA ────────────────────────────────────────────────
        # Two modes: "Type" (text input) or "Transcribe (voice)" (Whisper STT)
        answer_format = st.selectbox(
            "How do you want to answer?",
            options=["Type", "Transcribe (voice)"],
            label_visibility="collapsed"
        )

        if answer_format == "Type":
            # ── Typed answer mode ──
            # Uses a dynamic key (session_id + turn_index) so the input
            # clears automatically when a new turn starts.
            turn_index = len(st.session_state.conversation)
            sid = st.session_state.interview_session_id
            user_answer = st.text_input(
                "Your answer",
                key=f"typed_answer_{sid}_{turn_index}",
                placeholder="Type your response here..."
            )
            if st.button("📤  Send Answer", use_container_width=True):
                if not user_answer:
                    st.warning("Please type an answer first.")
                else:
                    with st.spinner(f"Sending to {iname}..."):
                        try:
                            send_answer(user_answer)
                        except ValueError as e:
                            st.error(str(e))

        else:
            # ── Voice answer mode (Whisper transcription) ──
            # 1. Load Whisper model (cached)
            # 2. Record audio via st.audio_input
            # 3. Transcribe with Whisper
            # 4. Optionally auto-send, or show preview + manual send button

            processor, model = load_whisper()

            # Auto-send toggle: skips the preview step
            auto_send = st.checkbox(
                "Auto-send after transcription",
                value=st.session_state.auto_send_voice
            )
            st.session_state.auto_send_voice = auto_send

            # Audio recorder widget (dynamic key resets widget between turns)
            turn_idx = len(st.session_state.conversation)
            audio_file = st.audio_input("Record your answer", key=f"audio_rec_{st.session_state.interview_session_id}_{turn_idx}")

            if audio_file:
                raw_bytes = audio_file.read()
                audio_hash = hashlib.md5(raw_bytes).hexdigest()

                # Only process if this is a NEW recording (different hash)
                # This prevents re-transcription when Streamlit reruns
                if audio_hash != st.session_state.processed_audio_hash:
                    st.session_state.processed_audio_hash = audio_hash

                    with st.spinner("Transcribing your recording..."):
                        tmp_path = None
                        try:
                            # Save audio to a temp WAV file for processing
                            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                            tmp_path = tmp.name
                            tmp.write(raw_bytes)
                            tmp.close()

                            # Read audio and convert to mono 16kHz (Whisper's expected format)
                            waveform, sample_rate = sf.read(tmp_path)
                            if len(waveform.shape) > 1:
                                waveform = waveform.mean(axis=1)  # Stereo → mono
                            waveform = librosa.resample(
                                waveform, orig_sr=sample_rate, target_sr=16000
                            )

                            # Run Whisper inference
                            inputs = processor(waveform, sampling_rate=16000, return_tensors="pt")
                            with torch.no_grad():
                                predicted_ids = model.generate(inputs.input_features)
                            transcription = processor.batch_decode(
                                predicted_ids, skip_special_tokens=True
                            )[0]

                        except Exception as e:
                            # On error, reset hash so user can retry
                            st.session_state.processed_audio_hash = None
                            st.session_state.pending_transcription = None
                            st.error(f"Error processing audio: {e}")
                            transcription = ""
                        finally:
                            # Always clean up the temp file
                            if tmp_path and os.path.exists(tmp_path):
                                os.unlink(tmp_path)

                    if transcription.strip():
                        st.session_state.pending_transcription = transcription.strip()
                        if auto_send:
                            # Auto-send: immediately send without preview
                            with st.spinner(f"Sending to {iname}..."):
                                try:
                                    send_answer(st.session_state.pending_transcription)
                                except ValueError as e:
                                    st.error(str(e))
                    else:
                        # Empty transcription - reset hash so user can re-record
                        st.session_state.processed_audio_hash = None
                        if not transcription == "":
                            st.warning("Could not transcribe audio. Please try again.")

            # ── Manual send: show transcription preview + send button ──
            if st.session_state.pending_transcription and not auto_send:
                st.success(f"Transcribed: \"{st.session_state.pending_transcription}\"")
                if st.button("📤  Send Recording", use_container_width=True):
                    with st.spinner(f"Sending to {iname}..."):
                        try:
                            send_answer(st.session_state.pending_transcription)
                        except ValueError as e:
                            st.error(str(e))
