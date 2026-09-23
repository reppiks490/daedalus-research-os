from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "icarus-candidate-v1"


def export_candidate(path: Path, candidate: dict[str, Any]) -> Path:
    """Export a research-only manifest to the caller's chosen artifact path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": SCHEMA_VERSION,
        "status": "RESEARCH_CANDIDATE_ONLY",
        "production_authorized": False,
        "candidate": {**candidate, "production_authorized": False},
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")
    return path
