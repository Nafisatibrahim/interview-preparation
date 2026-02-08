from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os
from elevenlabs.play import play


# Load .env variables
load_dotenv()

# Function to convert text to audio bytes
def speak_text(
    text: str,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128"
):
    """
    Converts text to speech using ElevenLabs and returns audio bytes.
    """

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is not set. Make sure your .env file exists in the project folder."
        )

    # Create client inside the function to avoid scope issues
    client = ElevenLabs(api_key=api_key)

    audio_bytes = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format
    )
    # The SDK returns a generator; convert it to bytes
    audio_generator = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format
    )

    audio_bytes = b"".join(audio_generator)  # collect generator into bytes
    return audio_bytes


