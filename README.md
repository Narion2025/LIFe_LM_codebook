# LIFe_LM_codebook

Modulare Projektarchitektur für ein KI-gestütztes Codebook-System.
Die einzelnen Ordner lassen sich leicht erweitern und ermöglichen so eine
schrittweise Entwicklung weiterer Module.

## Setup

Diese Anwendung erfordert Python 3.11 oder höher und funktioniert sowohl unter
Windows 11 als auch unter macOS 13 oder neuer. Die empfohlenen Schritte sind:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Alle Skripte sind plattformunabhängig umgesetzt und verwenden ausschließlich
Standardbibliotheken beziehungsweise plattformneutrale Pakete.

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

## Funktionsweise

Die Anwendung gliedert sich in drei Kernmodule und eine GUI:

1. **Transcriber (`core/audio_input/transcriber.py`)** – wandelt Audiodateien
   per Whisper-API in Text um. Über die Checkbox "Lokale Transkription" in der
   Oberfläche kann stattdessen *Faster‑Whisper* ohne Internet genutzt werden.
2. **Marker-Parser (`core/gpt_semantics/gpt_marker_parser.py`)** – sendet den
   Text an ein GPT‑Modell (Standard `gpt-4`) und erhält die Marker als YAML.
3. **Exporter (`core/export/marker_exporter.py`)** – schreibt die Ergebnisse als
   YAML oder JSONL, z. B. nach `core/marker_model/` bzw.
   `exports/markers.jsonl`.

Die browserbasierte Oberfläche `frontend/streamlit_gui/streamlit_app.py`
steuert diese Schritte und zeigt die extrahierten Marker direkt an.

```
 Text/Eingabe ─┐
               v
         [transcriber.py]
               v
     [gpt_marker_parser.py]
               v
        [marker_exporter.py]
          │          │
          │          ├─▶ core/marker_model/*.yaml
          └──────────┴─▶ exports/markers.jsonl
```

## Quick Start


1. Abhängigkeiten installieren: `pip install -r requirements.txt`
2. `OPENAI_API_KEY` als Umgebungsvariable setzen, damit Transkription und GPT-Zugriff funktionieren.
3. Die GUI starten mit `streamlit run frontend/streamlit_gui/streamlit_app.py`.
   Über die Checkbox kann optional die lokale Whisper-Transkription genutzt werden (benötigt `faster-whisper`).
4. Konsistenz der YAML-Dateien lässt sich prüfen mit `python -m core.marker_model.validate_codebook`.

### Hinweis zu `openai`

Diese Anwendung verwendet die neue [OpenAI Python-Clientbibliothek](https://github.com/openai/openai-python) ab Version 1.0.
Alle API-Aufrufe erfolgen daher über ein `OpenAI`-Clientobjekt, z.B.:

```python
import openai
client = openai.OpenAI(api_key="...your key...")
client.models.list()
```

Falls versehentlich eine ältere Bibliotheksversion installiert ist, kann es zu Fehlern wie "Invalid Key" kommen. Installiere deshalb immer die Version aus `requirements.txt`.


## Installer

Für nicht-technische Anwender gibt es das Skript `installer/install_gui.py`. Es installiert alle benötigten Pakete und fragt über eine kleine GUI den `OPENAI_API_KEY` ab. Eine vorhandene `.env`-Datei kann importiert werden. Nach erfolgreicher Validierung wird der Schlüssel in `.env` gespeichert.

Unter macOS startet man das Tool per Doppelklick auf `start_mac.command`, unter Windows über `start_windows.bat`.
## Schritt-für-Schritt-Anleitung (macOS)

1. **Python 3.11 installieren:**
   `brew install python@3.11`
2. **Virtuelle Umgebung anlegen und aktivieren:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```
3. **Abhängigkeiten installieren:**
   `pip install -r requirements.txt`
4. **OpenAI-Schlüssel setzen (falls API genutzt wird):**
   `export OPENAI_API_KEY=<dein_schluessel>`
5. **GUI starten:**
   `streamlit run frontend/streamlit_gui/streamlit_app.py`

## Schritt-für-Schritt-Anleitung (Windows 11)

1. **Python 3.11 installieren:** Die offizielle Version gibt es auf
   [python.org](https://www.python.org/downloads/). Während der Installation
   "Add Python to PATH" aktivieren.
2. **Virtuelle Umgebung anlegen und aktivieren:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Abhängigkeiten installieren:**
   `pip install -r requirements.txt`
4. **OpenAI-Schlüssel setzen (optional):**
   `set OPENAI_API_KEY=<dein_schluessel>`
5. **GUI starten:**
   ```cmd
   streamlit run frontend/streamlit_gui/streamlit_app.py
```

## Streamlit Deployment

1. Repository auf GitHub hochladen.
2. Auf [Streamlit Cloud](https://streamlit.io/cloud) ein neues Projekt anlegen
   und dieses Repository verbinden.
3. Als Hauptdatei `frontend/streamlit_gui/streamlit_app.py` angeben und
   den `OPENAI_API_KEY` in den Secrets hinterlegen.

## Ideen für Erweiterungen

1. **Automatisierter Datenimport:** Ein Skript könnte regelmäßig neue Text- oder Audiodateien aus definierten Ordnern einlesen und automatisch analysieren.
2. **Verbesserte Benutzeroberfläche:** Eine integrierte Fortschrittsanzeige und vereinfachte Eingabefelder würden die Bedienung insbesondere für nicht-technische Anwender erleichtern.
3. **Batch-Export mit Zeitplan:** Über einen Scheduler könnte das Tool periodisch alle gesammelten Marker in einen zentralen Speicher exportieren (z. B. Datenbank oder Cloud-Speicher).


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
