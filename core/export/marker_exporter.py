from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

import yaml


def export_yaml(data: Mapping, file_path: str | Path) -> None:
    """Export dictionary data to a YAML file."""
    path = Path(file_path)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


def export_jsonl(records: Iterable[Mapping], file_path: str | Path) -> None:
    """Export an iterable of dictionaries to a JSONL file."""
    path = Path(file_path)
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            json.dump(rec, f, ensure_ascii=False)
            f.write("\n")
