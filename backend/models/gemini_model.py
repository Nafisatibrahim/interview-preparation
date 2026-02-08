from google import genai
import os

client = None
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)


def load_prompt(prompt_name: str) -> str:
    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)
    prompt_path = os.path.join(project_root, "prompts", prompt_name)

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


INTERVIEWER_PROMPT = load_prompt("interviewer.txt")
INTERVIEWER_FEEDBACK_PROMPT = load_prompt("evaluation.txt")


def _get_client():
    global client
    if client is None:
        key = os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError("Missing API key. Please set the GOOGLE_API_KEY secret.")
        client = genai.Client(api_key=key)
    return client


def interview_response(
    job_description: str,
    resume_text: str,
    conversation_history: list,
    user_input: str,
    interviewer_name: str = "Stacy"
) -> str:
    history_text = ""
    for turn in conversation_history:
        history_text += f"{interviewer_name}: {turn['interviewer']}\n"
        history_text += f"Candidate: {turn['candidate']}\n"

    full_prompt = f"""
{INTERVIEWER_PROMPT}

Your name is {interviewer_name}. Introduce yourself by this name at the start of the interview.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Conversation so far:
{history_text}

Candidate just said:
{user_input}

Respond as {interviewer_name}, the interviewer.
"""

    response = _get_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
    )

    return response.text.strip()


def interview_feedback(
    job_description: str,
    resume_text: str,
    conversation_history: list,
) -> str:
    history_text = ""
    for turn in conversation_history:
        history_text += f"Interviewer: {turn['interviewer']}\n"
        history_text += f"Candidate: {turn['candidate']}\n"

    full_prompt = f"""
{INTERVIEWER_FEEDBACK_PROMPT}

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Conversation so far:
{history_text}

Provide professional interview feedback and evaluation of the candidate.
Include strengths, weaknesses, and concrete improvement suggestions.
"""

    response = _get_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
    )
    return response.text.strip()
