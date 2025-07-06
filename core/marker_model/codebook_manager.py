"""
Codebook Manager: Verwaltung und Pflege von Marker-, Indikatoren- und Meta-Indikatoren-YAML-Dateien
- Hinzufügen, Bearbeiten, Verlinken, Löschen
- Konsistenzprüfung der Referenzen
"""
import yaml
from pathlib import Path
from typing import List, Dict, Any

CODEBOOK_PATH = Path(__file__).parent
MARKER_FILE = CODEBOOK_PATH / "marker_library.yaml"
INDIKATOREN_FILE = CODEBOOK_PATH / "indikatoren.yaml"
META_FILE = CODEBOOK_PATH / "meta_indikatoren.yaml"

def load_yaml(file_path: Path) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(file_path: Path, data: Any):
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

# --- Marker ---
def add_marker(marker: Dict):
    data = load_yaml(MARKER_FILE) or {"marker_library": []}
    data["marker_library"].append(marker)
    save_yaml(MARKER_FILE, data)

def update_marker(marker_id: str, updates: Dict):
    data = load_yaml(MARKER_FILE)
    for m in data["marker_library"]:
        if m["id"] == marker_id:
            m.update(updates)
    save_yaml(MARKER_FILE, data)

# --- Indikatoren ---
def add_indikator(indikator: Dict):
    data = load_yaml(INDIKATOREN_FILE) or {"indikatoren": []}
    data["indikatoren"].append(indikator)
    save_yaml(INDIKATOREN_FILE, data)

def update_indikator(indikator_id: str, updates: Dict):
    data = load_yaml(INDIKATOREN_FILE)
    for i in data["indikatoren"]:
        if i["id"] == indikator_id:
            i.update(updates)
    save_yaml(INDIKATOREN_FILE, data)

# --- Meta-Indikatoren ---
def add_meta(meta: Dict):
    data = load_yaml(META_FILE) or {"meta_indikatoren": []}
    data["meta_indikatoren"].append(meta)
    save_yaml(META_FILE, data)

def update_meta(meta_id: str, updates: Dict):
    data = load_yaml(META_FILE)
    for m in data["meta_indikatoren"]:
        if m["id"] == meta_id:
            m.update(updates)
    save_yaml(META_FILE, data)

# --- Konsistenzprüfung ---
def check_consistency() -> Dict[str, List[str]]:
    """Prüft, ob alle Referenzen gültig sind."""
    marker = load_yaml(MARKER_FILE)["marker_library"]
    indikatoren = load_yaml(INDIKATOREN_FILE)["indikatoren"]
    meta = load_yaml(META_FILE)["meta_indikatoren"]
    errors = {"indikatoren": [], "meta": [], "marker": []}
    marker_ids = {m["id"] for m in marker}
    indikator_ids = {i["id"] for i in indikatoren}
    meta_ids = {m["id"] for m in meta}
    # Indikatoren prüfen
    for i in indikatoren:
        for mid in i.get("marker_ids", []):
            if mid not in marker_ids:
                errors["indikatoren"].append(f"Indikator {i['id']} referenziert unbekannten Marker {mid}")
        for meta_id in i.get("meta_indikatoren", []):
            if meta_id not in meta_ids:
                errors["indikatoren"].append(f"Indikator {i['id']} referenziert unbekannten Meta-Indikator {meta_id}")
    # Meta-Indikatoren prüfen
    for m in meta:
        for iid in m.get("indikator_ids", []):
            if iid not in indikator_ids:
                errors["meta"].append(f"Meta-Indikator {m['id']} referenziert unbekannten Indikator {iid}")
    # Marker prüfen
    for m in marker:
        for iid in m.get("linked_indicators", []):
            if iid not in indikator_ids:
                errors["marker"].append(f"Marker {m['id']} referenziert unbekannten Indikator {iid}")
    return errors

if __name__ == "__main__":
    # Beispiel: Konsistenzprüfung ausführen
    result = check_consistency()
    print("Konsistenzprüfung:")
    for k, v in result.items():
        if v:
            print(f"{k}:\n  " + "\n  ".join(v))
        else:
            print(f"{k}: OK")
