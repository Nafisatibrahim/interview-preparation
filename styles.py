GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #4F46E5;
    --primary-light: #818CF8;
    --primary-dark: #3730A3;
    --accent: #06B6D4;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --bg-main: #FAFBFC;
    --bg-card: #FFFFFF;
    --bg-sidebar: #F1F5F9;
    --text-primary: #1E293B;
    --text-secondary: #64748B;
    --text-muted: #94A3B8;
    --border: #E2E8F0;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05);
    --radius: 12px;
}

html, body, [class*="st-"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: var(--bg-main);
}

.block-container {
    padding-top: 2rem !important;
    max-width: 900px !important;
}

h1 {
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.2rem !important;
    margin-bottom: 0.5rem !important;
}

h2, h3 {
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #334155 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 20px rgba(0,0,0,0.1);
}

section[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] .stTextArea label,
section[data-testid="stSidebar"] .stFileUploader label {
    color: #94A3B8 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
}

section[data-testid="stSidebar"] .stTextInput input:focus,
section[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: var(--primary-light) !important;
    box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.3) !important;
}

section[data-testid="stSidebar"] .stFileUploader {
    background: rgba(255,255,255,0.05) !important;
    border: 2px dashed rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
    margin: 1.2rem 0 !important;
}

.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
    letter-spacing: -0.01em !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    width: 100% !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
    transform: translateY(-1px) !important;
}

.main .stButton > button {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}

.main .stButton > button:hover {
    background: #F8FAFC !important;
    border-color: var(--primary-light) !important;
    box-shadow: var(--shadow-md) !important;
}

.main .stTextInput input,
.main .stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.7rem 1rem !important;
    transition: all 0.2s ease !important;
    color: var(--text-primary) !important;
    background: var(--bg-card) !important;
}

.main .stSelectbox label,
.main .stTextInput label,
.main .stTextArea label,
.main .stCheckbox label span {
    color: var(--text-primary) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}

.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
}

.stRadio > div {
    gap: 0.5rem !important;
}

.stRadio label {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
}

.stExpander {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.2rem !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25) !important;
}

.stDownloadButton > button:hover {
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
}

div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
}

.stCheckbox label {
    font-family: 'Inter', sans-serif !important;
}

.stSpinner > div {
    border-color: var(--primary) transparent transparent transparent !important;
}

div.stAudio {
    border-radius: 10px !important;
    overflow: hidden !important;
}
</style>
"""

CHAT_HTML_TEMPLATE = """
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: transparent;
}}
.chat-container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-width: 800px;
    margin: 0 auto;
    padding: 16px 8px;
}}
.chat-bubble {{
    max-width: 78%;
    padding: 14px 18px;
    border-radius: 18px;
    line-height: 1.6;
    font-size: 0.92rem;
    word-wrap: break-word;
    position: relative;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}}
.chat-bubble-left {{
    align-self: flex-start;
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    border: 1px solid #E2E8F0;
    border-bottom-left-radius: 4px;
    color: #1E293B;
}}
.chat-bubble-right {{
    align-self: flex-end;
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
    border-bottom-right-radius: 4px;
    color: #FFFFFF;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2);
}}
.chat-meta {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}}
.chat-avatar {{
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    flex-shrink: 0;
}}
.avatar-interviewer {{
    background: linear-gradient(135deg, #06B6D4, #0891B2);
    color: white;
}}
.avatar-user {{
    background: linear-gradient(135deg, #4F46E5, #6366F1);
    color: white;
}}
.chat-name {{
    font-weight: 600;
    font-size: 0.78rem;
    opacity: 0.75;
    letter-spacing: 0.01em;
}}
.chat-bubble-left .chat-name {{
    color: #475569;
}}
.chat-bubble-right .chat-name {{
    color: rgba(255,255,255,0.85);
}}
.q-number {{
    display: inline-block;
    background: rgba(79, 70, 229, 0.1);
    color: #4F46E5;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 10px;
    margin-left: auto;
}}
.chat-bubble-right .q-number {{
    background: rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.9);
}}
</style>
</head>
<body>
<div class="chat-container">
    {bubbles}
</div>
<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
</body>
</html>
"""

HERO_HTML = """
<div style="
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, rgba(79,70,229,0.04) 0%, rgba(6,182,212,0.04) 100%);
    border-radius: 20px;
    border: 1px solid rgba(79,70,229,0.08);
    margin-bottom: 2rem;
">
    <div style="font-size: 3rem; margin-bottom: 0.8rem;">🎯</div>
    <h2 style="
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.6rem;
        color: #1E293B;
        margin: 0 0 0.6rem 0;
        letter-spacing: -0.03em;
    ">Ace Your Next Interview</h2>
    <p style="
        font-family: 'Inter', sans-serif;
        color: #64748B;
        font-size: 1rem;
        max-width: 500px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    ">Upload your resume and paste the job description in the sidebar, then click <strong style='color: #4F46E5;'>Start Interview</strong> to begin your mock session.</p>
    <div style="
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            color: #64748B;
            font-size: 0.85rem;
            font-family: 'Inter', sans-serif;
        ">
            <span style="
                background: linear-gradient(135deg, #4F46E5, #6366F1);
                color: white;
                width: 28px; height: 28px;
                border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.8rem;
            ">1</span>
            Upload Resume
        </div>
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            color: #64748B;
            font-size: 0.85rem;
            font-family: 'Inter', sans-serif;
        ">
            <span style="
                background: linear-gradient(135deg, #4F46E5, #6366F1);
                color: white;
                width: 28px; height: 28px;
                border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.8rem;
            ">2</span>
            Paste Job Description
        </div>
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            color: #64748B;
            font-size: 0.85rem;
            font-family: 'Inter', sans-serif;
        ">
            <span style="
                background: linear-gradient(135deg, #4F46E5, #6366F1);
                color: white;
                width: 28px; height: 28px;
                border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.8rem;
            ">3</span>
            Start Interview
        </div>
    </div>
</div>
"""

SIDEBAR_HEADER_HTML = """
<div style="
    text-align: center;
    padding: 1.2rem 0.5rem 1rem 0.5rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
">
    <div style="
        font-size: 1.8rem;
        margin-bottom: 0.4rem;
    ">🎯</div>
    <div style="
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.1rem;
        background: linear-gradient(135deg, #818CF8, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    ">Prepy.ai</div>
</div>
"""

HOME_PAGE_HTML = """
<div style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">

    <!-- ═══════════ HERO SECTION ═══════════ -->
    <div style="
        text-align: center;
        padding: 3.5rem 2rem 3rem 2rem;
        background: linear-gradient(135deg, rgba(79,70,229,0.06) 0%, rgba(6,182,212,0.06) 100%);
        border-radius: 24px;
        border: 1px solid rgba(79,70,229,0.1);
        margin-bottom: 2.5rem;
    ">
        <div style="font-size: 3.5rem; margin-bottom: 0.6rem;">🎯</div>
        <h1 style="
            font-weight: 900;
            font-size: 2.8rem;
            background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 0.4rem 0;
            letter-spacing: -0.04em;
            line-height: 1.1;
        ">Prepy.ai</h1>
        <p style="
            color: #64748B;
            font-size: 1.15rem;
            max-width: 600px;
            margin: 0 auto 1.5rem auto;
            line-height: 1.7;
            font-weight: 400;
        ">Your AI-powered mock interview coach. Upload your resume, paste the job description, and practice with a realistic interviewer - powered by Google Gemini.</p>
        <div style="
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        ">
            <span style="
                background: rgba(79,70,229,0.1);
                color: #4F46E5;
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 0.82rem;
                font-weight: 600;
            ">AI-Powered</span>
            <span style="
                background: rgba(6,182,212,0.1);
                color: #0891B2;
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 0.82rem;
                font-weight: 600;
            ">Voice & Text</span>
            <span style="
                background: rgba(16,185,129,0.1);
                color: #059669;
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 0.82rem;
                font-weight: 600;
            ">Instant Feedback</span>
        </div>
    </div>

    <!-- ═══════════ DEMO VIDEO SECTION ═══════════ -->
    <div style="
        margin-bottom: 2.5rem;
    ">
        <h2 style="
            font-weight: 800;
            font-size: 1.3rem;
            color: #1E293B;
            margin: 0 0 1rem 0;
            letter-spacing: -0.02em;
            text-align: center;
        ">See It In Action</h2>
        <div style="
            background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
            border: 2px dashed #CBD5E1;
            border-radius: 16px;
            padding: 3rem 2rem;
            text-align: center;
            color: #94A3B8;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🎬</div>
            <p style="
                font-size: 1rem;
                margin: 0 0 0.5rem 0;
                color: #64748B;
                font-weight: 500;
            ">Demo video coming soon</p>
            <p style="
                font-size: 0.85rem;
                margin: 0;
                color: #94A3B8;
            ">A walkthrough video will be added here to show how Prepy.ai works</p>
        </div>
    </div>

    <!-- ═══════════ FEATURES SECTION ═══════════ -->
    <div style="margin-bottom: 2.5rem;">
        <h2 style="
            font-weight: 800;
            font-size: 1.3rem;
            color: #1E293B;
            margin: 0 0 1.2rem 0;
            letter-spacing: -0.02em;
            text-align: center;
        ">Features</h2>
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1rem;
        ">
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem 1.2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🤖</div>
                <h3 style="font-weight: 700; font-size: 0.95rem; color: #1E293B; margin: 0 0 0.3rem 0;">AI Interviewer</h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0; line-height: 1.5;">Powered by Google Gemini - asks realistic, role-specific questions based on your resume and job description.</p>
            </div>
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem 1.2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎤</div>
                <h3 style="font-weight: 700; font-size: 0.95rem; color: #1E293B; margin: 0 0 0.3rem 0;">Voice Answers</h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0; line-height: 1.5;">Record your answers and let Whisper transcribe them - or simply type your responses.</p>
            </div>
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem 1.2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔊</div>
                <h3 style="font-weight: 700; font-size: 0.95rem; color: #1E293B; margin: 0 0 0.3rem 0;">Interviewer Voice</h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0; line-height: 1.5;">Hear the interviewer speak using ElevenLabs text-to-speech for a more realistic experience.</p>
            </div>
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem 1.2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
                <h3 style="font-weight: 700; font-size: 0.95rem; color: #1E293B; margin: 0 0 0.3rem 0;">Detailed Feedback</h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0; line-height: 1.5;">Get a comprehensive performance report with strengths, weaknesses, and actionable improvement tips.</p>
            </div>
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem 1.2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📄</div>
                <h3 style="font-weight: 700; font-size: 0.95rem; color: #1E293B; margin: 0 0 0.3rem 0;">Resume Analysis</h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0; line-height: 1.5;">Upload your PDF resume and the AI tailors questions to your specific experience and skills.</p>
            </div>
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem 1.2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎨</div>
                <h3 style="font-weight: 700; font-size: 0.95rem; color: #1E293B; margin: 0 0 0.3rem 0;">Custom Interviewer</h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0; line-height: 1.5;">Name your interviewer and customize the experience. The AI adapts its persona accordingly.</p>
            </div>
        </div>
    </div>

    <!-- ═══════════ HOW IT WORKS ═══════════ -->
    <div style="margin-bottom: 2.5rem;">
        <h2 style="
            font-weight: 800;
            font-size: 1.3rem;
            color: #1E293B;
            margin: 0 0 1.2rem 0;
            letter-spacing: -0.02em;
            text-align: center;
        ">How It Works</h2>
        <div style="
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        ">
            <div style="
                text-align: center;
                max-width: 180px;
            ">
                <div style="
                    background: linear-gradient(135deg, #4F46E5, #6366F1);
                    color: white;
                    width: 44px; height: 44px;
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                    font-weight: 800;
                    margin: 0 auto 0.6rem auto;
                    box-shadow: 0 4px 12px rgba(79,70,229,0.3);
                ">1</div>
                <p style="font-size: 0.85rem; color: #475569; font-weight: 600; margin: 0 0 0.2rem 0;">Upload Resume</p>
                <p style="font-size: 0.78rem; color: #94A3B8; margin: 0; line-height: 1.4;">Upload your PDF resume in the sidebar</p>
            </div>
            <div style="
                text-align: center;
                max-width: 180px;
            ">
                <div style="
                    background: linear-gradient(135deg, #4F46E5, #6366F1);
                    color: white;
                    width: 44px; height: 44px;
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                    font-weight: 800;
                    margin: 0 auto 0.6rem auto;
                    box-shadow: 0 4px 12px rgba(79,70,229,0.3);
                ">2</div>
                <p style="font-size: 0.85rem; color: #475569; font-weight: 600; margin: 0 0 0.2rem 0;">Add Job Description</p>
                <p style="font-size: 0.78rem; color: #94A3B8; margin: 0; line-height: 1.4;">Paste the target job description</p>
            </div>
            <div style="
                text-align: center;
                max-width: 180px;
            ">
                <div style="
                    background: linear-gradient(135deg, #4F46E5, #6366F1);
                    color: white;
                    width: 44px; height: 44px;
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                    font-weight: 800;
                    margin: 0 auto 0.6rem auto;
                    box-shadow: 0 4px 12px rgba(79,70,229,0.3);
                ">3</div>
                <p style="font-size: 0.85rem; color: #475569; font-weight: 600; margin: 0 0 0.2rem 0;">Practice</p>
                <p style="font-size: 0.78rem; color: #94A3B8; margin: 0; line-height: 1.4;">Answer questions via text or voice</p>
            </div>
            <div style="
                text-align: center;
                max-width: 180px;
            ">
                <div style="
                    background: linear-gradient(135deg, #10B981, #059669);
                    color: white;
                    width: 44px; height: 44px;
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                    font-weight: 800;
                    margin: 0 auto 0.6rem auto;
                    box-shadow: 0 4px 12px rgba(16,185,129,0.3);
                ">4</div>
                <p style="font-size: 0.85rem; color: #475569; font-weight: 600; margin: 0 0 0.2rem 0;">Get Feedback</p>
                <p style="font-size: 0.78rem; color: #94A3B8; margin: 0; line-height: 1.4;">Receive a detailed performance report</p>
            </div>
        </div>
    </div>

    <!-- ═══════════ FUTURE IMPROVEMENTS ═══════════ -->
    <div style="margin-bottom: 2.5rem;">
        <h2 style="
            font-weight: 800;
            font-size: 1.3rem;
            color: #1E293B;
            margin: 0 0 1rem 0;
            letter-spacing: -0.02em;
            text-align: center;
        ">Roadmap &amp; Future Improvements</h2>
        <div style="
            background: linear-gradient(135deg, rgba(79,70,229,0.03) 0%, rgba(6,182,212,0.03) 100%);
            border: 1px solid rgba(79,70,229,0.08);
            border-radius: 14px;
            padding: 1.5rem;
        ">
            <div style="display: flex; flex-direction: column; gap: 0.7rem;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #94A3B8; font-size: 0.9rem;">&#9744;</span>
                    <span style="font-size: 0.88rem; color: #475569;">Multiple interview types (behavioral, technical, case study)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #94A3B8; font-size: 0.9rem;">&#9744;</span>
                    <span style="font-size: 0.88rem; color: #475569;">Save &amp; review past interview sessions</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #94A3B8; font-size: 0.9rem;">&#9744;</span>
                    <span style="font-size: 0.88rem; color: #475569;">Progress tracking across multiple practice sessions</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #94A3B8; font-size: 0.9rem;">&#9744;</span>
                    <span style="font-size: 0.88rem; color: #475569;">Video recording &amp; body language analysis</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #94A3B8; font-size: 0.9rem;">&#9744;</span>
                    <span style="font-size: 0.88rem; color: #475569;">Industry-specific question banks</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #94A3B8; font-size: 0.9rem;">&#9744;</span>
                    <span style="font-size: 0.88rem; color: #475569;">Multi-language support</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ═══════════ TEAM / CONTRIBUTORS ═══════════ -->
    <div style="margin-bottom: 2.5rem;">
        <h2 style="
            font-weight: 800;
            font-size: 1.3rem;
            color: #1E293B;
            margin: 0 0 1rem 0;
            letter-spacing: -0.02em;
            text-align: center;
        ">Team</h2>
        <p style="font-size: 0.85rem; color: #64748B; margin: 0 0 1rem 0; text-align: center;">University of Waterloo</p>
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            max-width: 600px;
            margin: 0 auto;
        ">
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="
                    width: 50px; height: 50px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #4F46E5, #818CF8);
                    display: flex; align-items: center; justify-content: center;
                    margin: 0 auto 0.7rem auto;
                    font-size: 1.2rem;
                    color: white;
                    font-weight: 700;
                ">NI</div>
                <p style="font-weight: 700; font-size: 0.92rem; color: #1E293B; margin: 0 0 0.2rem 0;">Nafisat Ibrahim</p>
                <p style="font-size: 0.8rem; color: #94A3B8; margin: 0 0 0.5rem 0;">MMath in Data Science</p>
                <div style="display: flex; justify-content: center; gap: 0.8rem; margin-top: 0.4rem;">
                    <a href="https://nafisatibrahim.com/" target="_blank" style="font-size: 0.78rem; color: #4F46E5; text-decoration: none;">Website</a>
                    <a href="https://www.linkedin.com/in/nafisatibrahim/" target="_blank" style="font-size: 0.78rem; color: #4F46E5; text-decoration: none;">LinkedIn</a>
                </div>
            </div>
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 1.3rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <div style="
                    width: 50px; height: 50px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #06B6D4, #0891B2);
                    display: flex; align-items: center; justify-content: center;
                    margin: 0 auto 0.7rem auto;
                    font-size: 1.2rem;
                    color: white;
                    font-weight: 700;
                ">NH</div>
                <p style="font-weight: 700; font-size: 0.92rem; color: #1E293B; margin: 0 0 0.2rem 0;">Nigar Hajiyeva</p>
                <p style="font-size: 0.8rem; color: #94A3B8; margin: 0 0 0.5rem 0;">Exchange Student, Degree TBD</p>
                <div style="display: flex; justify-content: center; gap: 0.8rem; margin-top: 0.4rem;">
                    <span style="font-size: 0.78rem; color: #94A3B8;">Website TBD</span>
                    <a href="https://www.linkedin.com/in/nigar-hajiyeva-3883a8277/" target="_blank" style="font-size: 0.78rem; color: #4F46E5; text-decoration: none;">LinkedIn</a>
                </div>
            </div>
        </div>
    </div>

    <!-- ═══════════ GITHUB / LINKS ═══════════ -->
    <div style="
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-bottom: 1rem;
    ">
        <p style="
            color: #E2E8F0;
            font-size: 0.95rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        ">Open Source</p>
        <p style="
            color: #94A3B8;
            font-size: 0.85rem;
            margin: 0 0 0.8rem 0;
        ">Check out the source code and contribute on GitHub</p>
        <span style="
            display: inline-block;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.15);
            color: #CBD5E1;
            padding: 8px 20px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 500;
        ">GitHub link coming soon</span>
    </div>

</div>
"""
