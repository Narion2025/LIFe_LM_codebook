# User Experience Test Notes

This document summarizes the end-to-end test of the **LIFe_LM** prototype.

## Installation
1. Ensure Python 3.11+ is available.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) provide an `OPENAI_API_KEY` as environment variable for GPT and Whisper API usage.

## Configuration Options
- `OPENAI_API_KEY` – required for online transcription and GPT marker parsing.
- Local transcription via `faster-whisper` can be enabled in the Streamlit UI using the checkbox `Lokale Transkription nutzen`.

## Validation
The codebook YAML files can be checked with:
```bash
python -m core.marker_model.validate_codebook
```
Example output shows missing references and helps keep the dataset consistent.

## Creating YAML Entries
The `core.marker_model.codebook_manager` module provides helper functions:
- `add_marker`, `add_indikator`, `add_meta`
- `update_marker`, `update_indikator`, `update_meta`
- `check_consistency`

Using these helpers new markers and indicators are persisted to the YAML files.

## Test Summary
`pytest` runs two unit tests:
1. `tests/test_openai_api.py` – verifies the OpenAI client API.
2. `tests/test_codebook_manager.py` – exercises adding markers and indicators in a temporary workspace and checks consistency.

Both tests pass after installation.
