import streamlit as st
from backend.models.gemini_model_old import interview_response
from backend.models.gemini_model_old import interview_feedback

from backend.pdf_reader import extract_text_from_pdf
from backend.models.audio_tts_old import speak_text


import torch
import soundfile as sf
import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration


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
st.sidebar.subheader("Input your materials")

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
    st.session_state.resume_text = resume_text
    st.success("Resume uploaded and read successfully.")
    st.pdf(resume_pdf)
# Start interview
if st.sidebar.button("Start Interview"):
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
flag = False
# Conversation UI
if st.session_state.started and not flag:
    st.subheader("Interview")

    for turn in st.session_state.conversation:
        st.markdown(f"**Interviewer:** {turn['interviewer']}")
        if turn["candidate"]:
            st.markdown(f"**You:** {turn['candidate']}")

   
 
    @st.cache_resource

    def load_whisper():
            processor = WhisperProcessor.from_pretrained("openai/whisper-small")
            model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
            model.config.forced_decoder_ids = None
            return processor, model

    processor, model = load_whisper()


    format = st.selectbox("Do you want to answer with transcription or type your answers?", options =
                    ["Transcribe", "Type"])

    if format=="Type":
        user_answer = st.text_input("Your answer")
    else:
        audio_file = st.audio_input("Speak your answer")

        if audio_file:
                

            # 1. Read audio bytes into waveform
            audio_bytes = audio_file.read()

            # Save to temp wav (simplest reliable way)
            with open("temp.wav", "wb") as f:
                f.write(audio_bytes)

            # 2. Load waveform properly
            waveform, sample_rate = sf.read("temp.wav")

            # Convert stereo → mono
            if len(waveform.shape) > 1:
                waveform = waveform.mean(axis=1)

            
            waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=16000)


            inputs = processor(waveform, sampling_rate=16000, return_tensors="pt")

            with torch.no_grad():
                predicted_ids = model.generate(inputs.input_features)

            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    if st.button("Send Answer"):
        if format=="Type":
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
                audio_bytes = speak_text(next_response)
                st.audio(audio_bytes, format="audio/mp3") 

                st.session_state.conversation.append({
                    "interviewer": next_response,
                    "candidate": ""
                })
        else:
            if not transcription:
                st.warning("Please enter or speak an answer.")
            else:
                st.session_state.conversation[-1]["candidate"] = transcription

                next_response = interview_response(
                    st.session_state.job_description,
                    st.session_state.resume_text,
                    st.session_state.conversation,
                    transcription
                )
                audio_bytes = speak_text(next_response)
                st.audio(audio_bytes, format="audio/mp3") 
                st.session_state.conversation.append({
                    "interviewer": next_response,
                    "candidate": ""
                })

st.sidebar.subheader("End the Interview and Get Feedback ")
if st.sidebar.button("Stop Interview"):
    flag = True
    next_response = interview_feedback(
        st.session_state.job_description,
        st.session_state.resume_text,
        st.session_state.conversation,
    )
    print("da")
    st.audio(audio_bytes, format="audio/mp3",start_time = "5s") 
    st.subheader("Feedback")
    st.write(next_response)