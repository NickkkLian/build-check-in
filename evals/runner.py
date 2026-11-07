"""Shared unchanged input helpers from the earlier evaluation runner."""
import json
from pathlib import Path

def raw_evidence(history):
    # Both arms get the same raw diffs. No attribution labels, consent conclusion,
    # safe public brief, warnings or claim judgments are included in this bundle.
    lines = ["# Raw file changes (private, not executed)"]
    for item in history["evidence"]:
        if item["kind"] == "diff":
            lines.append(json.dumps({key: item[key] for key in ("id", "file", "added", "removed")}, ensure_ascii=False))
    return "\n\n".join(lines) + "\n"


def ignore(directory, names):
    return {name for name in names if name in {"node_modules", "__pycache__", ".venv"} or (Path(directory) / name).is_symlink()}


