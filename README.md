# LIFe_LM_codebook

Modulare Projektarchitektur für ein KI-gestütztes Codebook-System.
Die einzelnen Ordner lassen sich leicht erweitern und ermöglichen so eine
schrittweise Entwicklung weiterer Module.

## Verzeichnisstruktur

- core/
  - audio_input/              # Speech-to-Text (OpenAI Whisper API + optional lokal)
  - gpt_semantics/            # GPT-gestützte Marker-Extraktion
  - marker_model/             # YAML-Schema-Verwaltung (Marker, Indikator, Meta)
  - export/                   # JSONL, YAML, CSV
- frontend/
  - streamlit_gui/            # Browserbasierte Benutzeroberfläche (Speech + Text + Vorschau)
- visualization/
  - semantic_graph/           # Abhängigkeitsnetzwerk: Marker ↔ Indikatoren ↔ Meta-Indikatoren

## Funktionale Anforderungen

- Modulare Erweiterbarkeit
- KI-gestützte Extraktion und Visualisierung
- Export in verschiedene Formate
- Benutzerfreundliche Oberfläche
## Quick Start

1. Abhängigkeiten installieren: `pip install openai streamlit faster-whisper pyyaml`
2. `OPENAI_API_KEY` als Umgebungsvariable setzen, damit Transkription und GPT-Zugriff funktionieren.
3. Die GUI starten mit `streamlit run frontend/streamlit_gui/streamlit_app.py`.
   Über die Checkbox kann optional die lokale Whisper-Transkription genutzt werden (benötigt `faster-whisper`).
4. Konsistenz der YAML-Dateien lässt sich prüfen mit `python -m core.marker_model.validate_codebook`.


# Iterativer Projektplan

## Phase 1: Core-Prototyp
- Ziel: Minimal funktionsfähiges System für Spracheingabe, Marker-Extraktion und Export
- Tasks:
  1. Implementiere `transcriber.py` für Audio-zu-Text (Whisper API + lokal)
  2. Entwickle `gpt_marker_parser.py` für GPT-gestützte Marker-Extraktion
  3. Erstelle `marker_exporter.py` für Export in YAML & JSONL
  4. Baue `streamlit_app.py` als GUI (Textfeld & Audio-Upload)

## Phase 2: Codebuch-Architektur
- Ziel: Strukturierte, referenzielle Ablage der Marker, Indikatoren und Meta-Indikatoren
- Tasks:
  1. Lege `marker_library.yaml`, `indikatoren.yaml`, `meta_indikatoren.yaml` an
  2. Implementiere ID-Referenzierung & n:m-Verlinkung
  3. Pflege- und Update-Logik für Marker/Indikatoren

## Phase 3: Validierung & Konsistenzprüfung
- Ziel: Sicherstellung der Datenqualität und Nachvollziehbarkeit
- Tasks:
  1. YAML-Schema-Checker für alle Codebuchdateien
  2. Anzeige fehlender Marker pro Indikator
  3. Anzeige nicht verlinkter Marker

## Phase 4: Visualisierung
- Ziel: Interaktive Analyse der Marker- und Indikatorenbeziehungen
- Tasks:
  1. Graph-Visualisierung (networkx/pyvis)
  2. Filter- und Clusterfunktionen
  3. Lückenanalyse & Vorschläge via GPT

## Phase 5: Export & Fine-Tuning
- Ziel: Datenexport für LLM-Training und Framework-Scoring
- Tasks:
  1. JSONL-Batch-Exporter für Marker/Indikatoren
  2. Prompt-Pair-Generierung für LLM-Training
  3. Anbindung an Trainingsdatenbank (optional)

---

Jede Phase kann als Sprint/Iteration umgesetzt werden. Nach Abschluss einer Phase erfolgt Review & Planung der nächsten Iteration.