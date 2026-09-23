from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "icarus-candidate-v1"


def export_candidate(path: Path, candidate: dict[str, Any]) -> Path:
    """Export a read-only research candidate manifest. This function never writes into Icarus itself."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": SCHEMA_VERSION,
        "status": "RESEARCH_CANDIDATE_ONLY",
        "production_authorized": False,
        "candidate": candidate,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")
    return path
