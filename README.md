<p align="center">
  <img src="https://img.shields.io/badge/Hackathon-CXC%202026-orange?style=for-the-badge" alt="CXC 2026" />
  <img src="https://img.shields.io/badge/Powered%20by-Tangerine-yellow?style=for-the-badge" alt="Powered by Tangerine" />
  <img src="https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini" />
</p>

# Prepy.ai

**Your AI-powered mock interview coach.**

Upload your resume, paste the job description, and practice with a realistic AI interviewer - powered by Google Gemini, OpenAI Whisper, and ElevenLabs.

Built for the **CXC 2026 - AI Hackathon**, powered by Tangerine.

---

## Links

| Link | Description |
|------|-------------|
| [Live App (Streamlit Cloud)](https://interview-preparation-coach.streamlit.app/) | Try Prepy.ai right now |
| [Devpost Submission](https://devpost.com/software/interview-preparation-coach) | Hackathon project page |
| [GitHub Repository](https://github.com/Nafisatibrahim/interview-preparation) | Source code |

> **Demo Video:** Coming soon - a walkthrough video will be linked here.

---

## The Problem

Preparing for job interviews can be stressful, especially without access to a practice partner who can simulate realistic interview scenarios. Traditional mock interviews require scheduling with friends, mentors, or career coaches - and even then, the feedback is often inconsistent and subjective.

## Our Solution

Prepy.ai is an AI-powered mock interview tool that gives anyone instant access to a personalized, realistic interview experience. Simply upload your resume and paste the job description - the AI interviewer asks tailored questions, listens to your answers (via voice or text), and provides a detailed performance report with actionable feedback.

---

## Features

| Feature | Description |
|---------|-------------|
| **AI Interviewer** | Powered by Google Gemini - asks realistic, role-specific questions based on your resume and job description |
| **Voice Answers** | Record your answers using your microphone; Whisper (OpenAI) transcribes them automatically |
| **Interviewer Voice** | Hear the interviewer speak using ElevenLabs text-to-speech for a lifelike experience |
| **Detailed Feedback** | Get a comprehensive performance report with strengths, weaknesses, and improvement tips |
| **Resume Analysis** | Upload your PDF resume and the AI tailors questions to your specific experience and skills |
| **Custom Interviewer** | Name your interviewer and customize the experience (default: Stacy) |
| **Configurable Sessions** | Choose the number of interview questions (1-20) |

---

## How It Works

1. **Upload** - Upload your resume (PDF) and paste the job description
2. **Configure** - Set the interviewer name and number of questions
3. **Practice** - Answer questions via text or voice recording
4. **Get Feedback** - Receive a detailed performance report from the AI

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| [Streamlit](https://streamlit.io/) | Web application framework |
| [Google Gemini](https://ai.google.dev/) (gemini-2.5-flash) | AI-powered interview Q&A and feedback generation |
| [OpenAI Whisper](https://github.com/openai/whisper) | Speech-to-text for voice answer transcription |
| [ElevenLabs](https://elevenlabs.io/) | Text-to-speech for interviewer voice |
| [PyTorch](https://pytorch.org/) | ML framework (CPU) for running Whisper |
| [pdfplumber](https://github.com/jsvine/pdfplumber) | PDF text extraction from resumes |
| [pypdfium2](https://github.com/nicholasgasior/pypdfium2) | PDF page rendering as images |
| [librosa](https://librosa.org/) | Audio processing for voice recordings |

---

## Project Structure

```
interview-preparation/
├── app.py                          # Main Streamlit application
├── styles.py                       # CSS, HTML templates, home page content
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
├── backend/
│   ├── __init__.py
│   ├── pdf_reader.py               # PDF text extraction
│   ├── models/
│   │   ├── gemini_model.py         # Google Gemini AI for interview Q&A and feedback
│   │   └── audio_tts.py            # ElevenLabs text-to-speech
│   └── prompts/
│       ├── interviewer.txt         # System prompt for interview mode
│       └── evaluation.txt          # System prompt for feedback/evaluation mode
├── requirements.txt                # Python dependencies
├── .python-version                 # Python version (3.11)
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- A [Google AI API key](https://ai.google.dev/) (for Gemini)
- An [ElevenLabs API key](https://elevenlabs.io/) (for text-to-speech)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nafisatibrahim/interview-preparation.git
   cd interview-preparation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file or set the following environment variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```

   On Streamlit Cloud, add these as secrets in your app settings.

4. **Run the application**
   ```bash
   streamlit run app.py --server.port=5000 --server.address=0.0.0.0
   ```

5. Open your browser and navigate to `http://localhost:5000`

---

## Roadmap

- [ ] Multiple interview types (behavioral, technical, case study)
- [ ] Save and review past interview sessions
- [ ] Progress tracking across multiple practice sessions
- [ ] Video recording and body language analysis
- [ ] Industry-specific question banks
- [ ] Multi-language support

---

## Team

Built by students at the **University of Waterloo**.

### Nafisat Ibrahim
MMath in Data Science

[![Website](https://img.shields.io/badge/Website-nafisatibrahim.com-4F46E5?style=flat-square)](https://nafisatibrahim.com/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nafisat%20Ibrahim-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/nafisatibrahim/)
[![GitHub](https://img.shields.io/badge/GitHub-Nafisatibrahim-181717?style=flat-square&logo=github)](https://github.com/Nafisatibrahim)

### Nigar Hajiyeva
Exchange Student

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nigar%20Hajiyeva-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/nigar-hajiyeva-3883a8277/)

---

## Hackathon

This project was built for the **CXC 2026 - AI Hackathon**, powered by **Tangerine**.

CXC is Canada's largest student-run technology conference, hosted at the University of Waterloo. The AI Hackathon challenges participants to build innovative solutions using artificial intelligence.

---

## License

This project is open source. See the repository for license details.

---

<p align="center">
  Made with care at the University of Waterloo
</p>
