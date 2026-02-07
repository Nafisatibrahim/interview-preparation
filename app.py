import streamlit as st
from backend.gemini_model import gemini_simple_test

st.set_page_config(page_title="Interview Prep")

st.title("Interview Prep AI")

prompt = st.text_area("Enter a prompt")

if st.button("Send to Gemini"):
    if prompt:
        response = gemini_simple_test(prompt)
        st.write(response)
    else:
        st.warning("Please enter a prompt")
