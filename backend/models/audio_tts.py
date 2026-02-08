import os
from elevenlabs.client import ElevenLabs


def speak_text(
    text: str,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128"
):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is not set."
        )

    client = ElevenLabs(api_key=api_key)

    audio_generator = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format
    )

    audio_bytes = b"".join(audio_generator)
    return audio_bytes
