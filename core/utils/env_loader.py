"""Utility to load an OPENAI_API_KEY from a .env file."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def load_openai_key(env_path: str | Path = ".env") -> Optional[str]:
    """Load OPENAI_API_KEY from the given .env file and set it as env var."""
    path = Path(env_path)
    if not path.exists():
        return None
    key = None
    for line in path.read_text().splitlines():
        if line.startswith("OPENAI_API_KEY="):
            key = line.split("=", 1)[1].strip()
            break
    if key:
        os.environ.setdefault("OPENAI_API_KEY", key)
    return key
