import os
from typing import Optional

try:
    import openai
except ImportError:
    openai = None


PROMPT_TEMPLATE = (
    "Du bist ein hilfreicher Assistent, der aus Aussagen semantische Marker "
    "extrahiert. Gib das Ergebnis als YAML mit den Schluesseln "
    "indikator_id, marker_id, hinweis, typ, beispiel_aussage aus."
)


def parse_markers(text: str, api_key: Optional[str] = None, model: str = "gpt-4") -> str:
    """Send text to GPT model and return YAML string with markers."""
    if openai is None:
        raise ImportError("openai package is not installed")

    client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    messages = [
        {"role": "system", "content": PROMPT_TEMPLATE},
        {"role": "user", "content": text},
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()
