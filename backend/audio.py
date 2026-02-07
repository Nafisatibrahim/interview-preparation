import speech_recognition as sr
from pydub import AudioSegment
import tempfile

def transcribe_audio(audio_bytes) -> str:
    """
    Transcribe audio bytes to text.
    """
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        audio = AudioSegment.from_file(audio_bytes)
        audio.export(tmp.name, format="wav")

        with sr.AudioFile(tmp.name) as source:
            audio_data = recognizer.record(source)

        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return ""
