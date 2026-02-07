import streamlit as st
from backend.models.gemini_model import interview_response

st.set_page_config(page_title="Interview Prep AI")

st.title("🎤 Interview Prep AI")

# -----------------------
# Session state
# -----------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "started" not in st.session_state:
    st.session_state.started = False

# -----------------------
# Inputs
# -----------------------
job_description = st.text_area("Job Description")
resume_text = st.text_area("Resume")

if st.button("Start Interview"):
    if job_description and resume_text:
        st.session_state.started = True
        st.session_state.conversation = []

        first_question = interview_response(
            job_description,
            resume_text,
            [],
            "Start the interview."
        )

        st.session_state.conversation.append({
            "interviewer": first_question,
            "candidate": ""
        })
    else:
        st.warning("Please provide both job description and resume.")

# -----------------------
# Conversation UI
# -----------------------
if st.session_state.started:
    st.subheader("Interview")

    for turn in st.session_state.conversation:
        st.markdown(f"**Interviewer:** {turn['interviewer']}")
        if turn["candidate"]:
            st.markdown(f"**You:** {turn['candidate']}")

    user_answer = st.text_input("Your answer")

    if st.button("Send Answer"):
        if user_answer:
            st.session_state.conversation[-1]["candidate"] = user_answer

            next_response = interview_response(
                job_description,
                resume_text,
                st.session_state.conversation,
                user_answer
            )

            st.session_state.conversation.append({
                "interviewer": next_response,
                "candidate": ""
            })
        else:
            st.warning("Please enter an answer.")
