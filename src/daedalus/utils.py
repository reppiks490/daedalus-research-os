from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Any, Iterator

import numpy as np


@contextmanager
def sqlite_connection(path: Path) -> Iterator[sqlite3.Connection]:
    """Commit or roll back the transaction, then always close the handle."""
    with closing(sqlite3.connect(path)) as con:
        with con:
            yield con


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def stable_hash(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def finite_float(x: Any, default: float = 0.0) -> float:
    try:
        y = float(x)
        return y if np.isfinite(y) else default
    except (TypeError, ValueError):
        return default
