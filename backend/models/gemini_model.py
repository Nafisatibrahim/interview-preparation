# Test for Gemini Model
#from google import genai
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Configure Gemini 
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "Missing API key. Set GOOGLE_API_KEY"
    )

genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Load prompt from file
def load_prompt(prompt_name: str) -> str:
    """
    Load a prompt from the prompts/ directory.
    """
    current_dir = os.path.dirname(__file__)        # backend/
    project_root = os.path.dirname(current_dir)    # interview-preparation/
    prompt_path = os.path.join(project_root, "prompts", prompt_name)

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


# Load interviewer prompt
INTERVIEWER_PROMPT = load_prompt("interviewer.txt")

# Define Interview responses
def interview_response(
    job_description: str,
    resume_text: str,
    conversation_history: list,
    user_input: str
) -> str:
    """
    Generate the next interviewer response.
    """

    history_text = ""
    for turn in conversation_history:
        history_text += f"Interviewer: {turn['interviewer']}\n"
        history_text += f"Candidate: {turn['candidate']}\n"

    full_prompt = f"""
{INTERVIEWER_PROMPT}

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Conversation so far:
{history_text}

Candidate just said:
{user_input}

Respond as the interviewer.
"""

    response = model.generate_content(full_prompt)
    return response.text.strip()