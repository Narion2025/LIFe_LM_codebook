import os
from typing import Optional

try:
    import openai
except ImportError:  # openai might not be installed
    openai = None

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None


def transcribe_audio(audio_path: str, use_local: bool = False, api_key: Optional[str] = None) -> str:
    """Transcribe an audio file using OpenAI Whisper API or local Faster-Whisper."""
    if use_local:
        if WhisperModel is None:
            raise ImportError("faster_whisper is not installed")
        model = WhisperModel("base")
        segments, _ = model.transcribe(audio_path)
        return " ".join(seg.text.strip() for seg in segments)

    if openai is None:
        raise ImportError("openai package is not installed")

    client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(model="whisper-1", file=f)
    return response.text
