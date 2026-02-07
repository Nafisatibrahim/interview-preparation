# Test for Gemini Model
#from google import genai
import google.generativeai as genai
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Configure Gemini o
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "Missing API key. Set GOOGLE_API_KEY (preferred) or GEMINI_API_KEY."
    )
genai.configure(api_key=api_key)

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def gemini_simple_test(prompt: str) -> str:
    """
    Send a simple prompt to Gemini and return text output.
    """
    response = model.generate_content(prompt)
    return response.text
