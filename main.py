import streamlit as st
import streamlit.components.v1 as components
from backend.models.gemini_model import interview_response
from backend.models.gemini_model import interview_feedback
from backend.pdf_reader import extract_text_from_pdf
from backend.models.audio_tts import speak_text

import hashlib
import os
import tempfile
import torch
import soundfile as sf
import librosa
import pypdfium2 as pdfium
from transformers import WhisperProcessor, WhisperForConditionalGeneration

st.set_page_config(page_title="Interview Prep AI", layout="wide")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "started" not in st.session_state:
    st.session_state.started = False
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_pdf_bytes" not in st.session_state:
    st.session_state.resume_pdf_bytes = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "last_tts_audio" not in st.session_state:
    st.session_state.last_tts_audio = None
if "tts_played_for_turn" not in st.session_state:
    st.session_state.tts_played_for_turn = -1
if "processed_audio_hash" not in st.session_state:
    st.session_state.processed_audio_hash = None
if "interviewer_name" not in st.session_state:
    st.session_state.interviewer_name = "Stacy"
if "pending_transcription" not in st.session_state:
    st.session_state.pending_transcription = None
if "show_material" not in st.session_state:
    st.session_state.show_material = None
if "auto_send_voice" not in st.session_state:
    st.session_state.auto_send_voice = False
if "interview_session_id" not in st.session_state:
    st.session_state.interview_session_id = 0

st.title("Interview Prep AI")


def render_pdf_as_images(pdf_bytes, max_pages=5):
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
        st.download_button("Download Resume PDF", data=pdf_bytes, file_name="resume.pdf", mime="application/pdf", key="pdf_fallback")


def _escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_chat(conversation, interviewer_name):
    bubbles_html = ""
    for turn in conversation:
        interviewer_msg = _escape_html(turn['interviewer']).replace('\n', '<br>')
        bubbles_html += f"""
        <div class="chat-bubble chat-bubble-left">
            <div class="chat-name">{_escape_html(interviewer_name)}</div>
            {interviewer_msg}
        </div>
        """
        if turn["candidate"]:
            candidate_msg = _escape_html(turn['candidate']).replace('\n', '<br>')
            bubbles_html += f"""
            <div class="chat-bubble chat-bubble-right">
                <div class="chat-name">You</div>
                {candidate_msg}
            </div>
            """

    bubble_count = sum(1 + (1 if t["candidate"] else 0) for t in conversation)
    estimated_height = max(200, bubble_count * 120)

    full_html = f"""
    <html>
    <head>
    <style>
    body {{
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: transparent;
    }}
    .chat-container {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        max-width: 800px;
        margin: 0 auto;
        padding: 10px;
    }}
    .chat-bubble {{
        max-width: 75%;
        padding: 12px 16px;
        border-radius: 16px;
        line-height: 1.5;
        font-size: 0.95rem;
        word-wrap: break-word;
    }}
    .chat-bubble-left {{
        align-self: flex-start;
        background-color: #f0f2f6;
        border-bottom-left-radius: 4px;
        color: #1a1a1a;
    }}
    .chat-bubble-right {{
        align-self: flex-end;
        background-color: #25D366;
        border-bottom-right-radius: 4px;
        color: #ffffff;
    }}
    .chat-name {{
        font-weight: 700;
        font-size: 0.8rem;
        margin-bottom: 4px;
        opacity: 0.8;
    }}
    </style>
    </head>
    <body>
    <div class="chat-container">
        {bubbles_html}
    </div>
    </body>
    </html>
    """
    components.html(full_html, height=estimated_height, scrolling=True)


st.sidebar.subheader("Setup")

interviewer_name = st.sidebar.text_input(
    "Interviewer Name",
    value=st.session_state.interviewer_name
)
st.session_state.interviewer_name = interviewer_name

job_description_text = st.sidebar.text_area(
    "Job Description (paste text)",
    value=st.session_state.job_description
)

resume_pdf = st.sidebar.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = st.session_state.resume_text

if resume_pdf:
    resume_text = extract_text_from_pdf(resume_pdf)
    st.session_state.resume_pdf_bytes = resume_pdf.getvalue()
    if resume_text:
        st.session_state.resume_text = resume_text
        st.sidebar.success("Resume uploaded successfully.")
    else:
        st.sidebar.error("Could not read text from this PDF. Please try a different file.")

if st.sidebar.button("Start Interview"):
    if not job_description_text or not resume_text:
        st.warning("Please provide BOTH a job description and a resume.")
    else:
        try:
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

            first_question = interview_response(
                job_description_text,
                resume_text,
                [],
                "Start the interview.",
                interviewer_name=st.session_state.interviewer_name
            )

            try:
                tts_bytes = speak_text(first_question)
                st.session_state.last_tts_audio = tts_bytes
            except Exception:
                st.session_state.last_tts_audio = None

            st.session_state.conversation.append({
                "interviewer": first_question,
                "candidate": ""
            })
            st.rerun()
        except ValueError as e:
            st.error(str(e))
            st.session_state.started = False

st.sidebar.markdown("---")
st.sidebar.subheader("End Interview")
if st.sidebar.button("Stop Interview & Get Feedback"):
    if st.session_state.conversation:
        try:
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


@st.cache_resource
def load_whisper():
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    model.config.forced_decoder_ids = None
    return processor, model


def send_answer(answer_text):
    iname = st.session_state.interviewer_name
    if not st.session_state.conversation:
        st.warning("No interview in progress.")
        return
    st.session_state.conversation[-1]["candidate"] = answer_text

    next_resp = interview_response(
        st.session_state.job_description,
        st.session_state.resume_text,
        st.session_state.conversation,
        answer_text,
        interviewer_name=iname
    )

    try:
        tts_bytes = speak_text(next_resp)
        st.session_state.last_tts_audio = tts_bytes
    except Exception:
        st.session_state.last_tts_audio = None

    st.session_state.conversation.append({
        "interviewer": next_resp,
        "candidate": ""
    })

    st.session_state.pending_transcription = None
    st.session_state.tts_played_for_turn = -1
    st.rerun()


if not st.session_state.started and not st.session_state.feedback:
    st.markdown("### Welcome to Interview Prep AI")
    st.markdown("Upload your resume and paste a job description in the sidebar, then click **Start Interview** to begin your mock interview session.")

    if st.session_state.resume_pdf_bytes or job_description_text:
        view_option = st.radio(
            "Preview your materials",
            options=["Resume", "Job Description", "Side by Side"],
            horizontal=True
        )

        if view_option == "Resume":
            if st.session_state.resume_pdf_bytes:
                st.subheader("Your Resume")
                st.download_button("Download PDF", data=st.session_state.resume_pdf_bytes, file_name="resume.pdf", mime="application/pdf")
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
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Your Resume")
                if st.session_state.resume_pdf_bytes:
                    st.download_button("Download PDF", data=st.session_state.resume_pdf_bytes, file_name="resume.pdf", mime="application/pdf", key="dl_side")
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
    st.subheader("Interview Feedback")
    st.write(st.session_state.feedback)

elif st.session_state.started:
    iname = st.session_state.interviewer_name

    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 3])
    with btn_col1:
        if st.button("View Resume", use_container_width=True):
            st.session_state.show_material = "resume" if st.session_state.show_material != "resume" else None
            st.rerun()
    with btn_col2:
        if st.button("View Job Description", use_container_width=True):
            st.session_state.show_material = "jd" if st.session_state.show_material != "jd" else None
            st.rerun()

    if st.session_state.show_material == "resume" and st.session_state.resume_pdf_bytes:
        with st.expander("Resume", expanded=True):
            st.download_button("Download PDF", data=st.session_state.resume_pdf_bytes, file_name="resume.pdf", mime="application/pdf", key="dl_interview")
            render_pdf_as_images(st.session_state.resume_pdf_bytes)
    elif st.session_state.show_material == "jd" and st.session_state.job_description:
        with st.expander("Job Description", expanded=True):
            st.write(st.session_state.job_description)

    current_turn = len(st.session_state.conversation) - 1
    if st.session_state.last_tts_audio and st.session_state.tts_played_for_turn != current_turn:
        st.audio(st.session_state.last_tts_audio, format="audio/mp3", autoplay=True)
        st.session_state.tts_played_for_turn = current_turn

    render_chat(st.session_state.conversation, iname)

    st.markdown("---")

    answer_format = st.selectbox(
        "How do you want to answer?",
        options=["Type", "Transcribe (voice)"]
    )

    if answer_format == "Type":
        turn_index = len(st.session_state.conversation)
        sid = st.session_state.interview_session_id
        user_answer = st.text_input("Your answer", key=f"typed_answer_{sid}_{turn_index}")
        if st.button("Send Answer"):
            if not user_answer:
                st.warning("Please type an answer first.")
            else:
                with st.spinner(f"Sending to {iname}..."):
                    try:
                        send_answer(user_answer)
                    except ValueError as e:
                        st.error(str(e))
    else:
        processor, model = load_whisper()

        auto_send = st.checkbox("Auto-send after transcription", value=st.session_state.auto_send_voice)
        st.session_state.auto_send_voice = auto_send

        audio_file = st.audio_input("Record your answer")

        if audio_file:
            raw_bytes = audio_file.read()
            audio_hash = hashlib.md5(raw_bytes).hexdigest()

            if audio_hash != st.session_state.processed_audio_hash:
                st.session_state.processed_audio_hash = audio_hash

                with st.spinner("Transcribing your recording..."):
                    tmp_path = None
                    try:
                        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                        tmp_path = tmp.name
                        tmp.write(raw_bytes)
                        tmp.close()

                        waveform, sample_rate = sf.read(tmp_path)

                        if len(waveform.shape) > 1:
                            waveform = waveform.mean(axis=1)

                        waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=16000)

                        inputs = processor(waveform, sampling_rate=16000, return_tensors="pt")

                        with torch.no_grad():
                            predicted_ids = model.generate(inputs.input_features)

                        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
                    except Exception as e:
                        st.session_state.processed_audio_hash = None
                        st.session_state.pending_transcription = None
                        st.error(f"Error processing audio: {e}")
                        transcription = ""
                    finally:
                        if tmp_path and os.path.exists(tmp_path):
                            os.unlink(tmp_path)

                if transcription.strip():
                    st.session_state.pending_transcription = transcription.strip()
                    if auto_send:
                        with st.spinner(f"Sending to {iname}..."):
                            try:
                                send_answer(st.session_state.pending_transcription)
                            except ValueError as e:
                                st.error(str(e))
                else:
                    st.session_state.processed_audio_hash = None
                    if not transcription == "":
                        st.warning("Could not transcribe audio. Please try again.")

        if st.session_state.pending_transcription and not auto_send:
            st.success(f"Transcribed: \"{st.session_state.pending_transcription}\"")
            if st.button("Send Recording"):
                with st.spinner(f"Sending to {iname}..."):
                    try:
                        send_answer(st.session_state.pending_transcription)
                    except ValueError as e:
                        st.error(str(e))
