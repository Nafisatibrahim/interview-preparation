# TODO: Replace with your Gemini API setup
# Example:
# from google import genai
# from google.genai import types
# client = genai.Client(api_key="YOUR_API_KEY")
# MODEL = "gemini-2.5-flash"


def analyze_job_and_resume(job_description: str, resume: str) -> str:
    """Analyze job description against resume and return insights.

    TODO: Replace this placeholder with your Gemini API call.
    Should return a string with:
    - How well the candidate fits the role
    - Key strengths to highlight
    - Potential gaps to prepare for
    - Key topics likely to come up
    """
    return "**[Placeholder]** Connect your Gemini API to get a real analysis of your job fit, strengths, and areas to prepare."


def generate_interview_questions(job_description: str, resume: str, num_questions: int = 5) -> list[str]:
    """Generate interview questions based on job description and resume.

    TODO: Replace this placeholder with your Gemini API call.
    Should return a list of strings, each being an interview question.
    Mix behavioral, technical, situational, and culture fit questions.
    """
    return [
        "[Placeholder] Tell me about yourself and why you're interested in this role.",
        "[Placeholder] Describe a challenging project you worked on recently.",
        "[Placeholder] How do you handle tight deadlines and competing priorities?",
        "[Placeholder] What is your greatest professional achievement?",
        "[Placeholder] Where do you see yourself in five years?",
    ][:num_questions]


def evaluate_answer(question: str, answer: str, job_description: str) -> str:
    """Evaluate a candidate's answer to an interview question.

    TODO: Replace this placeholder with your Gemini API call.
    Should return a string with:
    - Score (1-10)
    - Strengths of the answer
    - Areas for improvement
    - Example of a strong answer
    """
    return "**[Placeholder]** Connect your Gemini API to get real feedback on your answer, including a score, strengths, and improvement tips."


def get_final_summary(questions: list[str], answers: list[str], feedbacks: list[str], job_description: str) -> str:
    """Generate a final summary of the entire mock interview.

    TODO: Replace this placeholder with your Gemini API call.
    Should return a string with:
    - Overall performance assessment
    - Top strengths across all answers
    - Priority areas for improvement
    - Preparation tips for the real interview
    - Confidence/readiness rating out of 10
    """
    return "**[Placeholder]** Connect your Gemini API to get a full performance summary with scores, strengths, and preparation tips."
