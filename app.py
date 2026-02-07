import streamlit as st
from backend.models.gemini_model import interview_response
from backend.pdf_reader import extract_text_from_pdf
# from backend.audio_utils import transcribe_audio  # add later

# Page config
st.set_page_config(page_title="Interview Prep AI")

st.title("🎤 Interview Prep AI")

# Session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "started" not in st.session_state:
    st.session_state.started = False

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# Input section
st.subheader("Input your materials")

job_description_text = st.text_area(
    "Job Description (paste text)",
    value=st.session_state.job_description
)

resume_pdf = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = st.session_state.resume_text

if resume_pdf:
    resume_text = extract_text_from_pdf(resume_pdf)
    st.session_state.resume_text = resume_text
    st.success("Resume uploaded and read successfully.")

# Start interview
if st.button("Start Interview"):
    if not job_description_text or not resume_text:
        st.warning("Please provide BOTH a job description and a resume.")
    else:
        st.session_state.started = True
        st.session_state.conversation = []
        st.session_state.job_description = job_description_text

        first_question = interview_response(
            job_description_text,
            resume_text,
            [],
            "Start the interview."
        )

        st.session_state.conversation.append({
            "interviewer": first_question,
            "candidate": ""
        })

# Conversation UI
if st.session_state.started:
    st.subheader("Interview")

    for turn in st.session_state.conversation:
        st.markdown(f"**Interviewer:** {turn['interviewer']}")
        if turn["candidate"]:
            st.markdown(f"**You:** {turn['candidate']}")

    user_answer = st.text_input("Your answer")

    # Audio input can be added here later
    # audio = st.audio_input("Speak your answer")
    # if audio:
    #     user_answer = transcribe_audio(audio)

    if st.button("Send Answer"):
        if not user_answer:
            st.warning("Please enter or speak an answer.")
        else:
            st.session_state.conversation[-1]["candidate"] = user_answer

            next_response = interview_response(
                st.session_state.job_description,
                st.session_state.resume_text,
                st.session_state.conversation,
                user_answer
            )

            st.session_state.conversation.append({
                "interviewer": next_response,
                "candidate": ""
            })
