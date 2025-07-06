import os
import tempfile

import streamlit as st

from core.audio_input.transcriber import transcribe_audio
from core.gpt_semantics.gpt_marker_parser import parse_markers


st.title("LIFe Codebook Prototype")

text_input = st.text_area("Text eingeben")
audio_file = st.file_uploader("Audio hochladen", type=["mp3", "wav"])
use_local = st.checkbox("Lokale Transkription nutzen", value=False)

if st.button("Analysieren"):
    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        text_input = transcribe_audio(tmp_path, use_local=use_local)
        os.unlink(tmp_path)

    if not text_input:
        st.warning("Bitte Text eingeben oder Audiodatei hochladen.")
    else:
        markers_yaml = parse_markers(text_input)
        st.subheader("Extrahierte Marker")
        st.code(markers_yaml, language="yaml")
