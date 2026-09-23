import json
import sys

import pandas as pd

from daedalus import cli
from daedalus.bridge import export_candidate


def test_catalog_cli_preserves_two_roots_with_same_named_file(tmp_path, monkeypatch, capsys):
    roots = [tmp_path / "clock", tmp_path / "heikin"]
    for root in roots:
        root.mkdir()
    frame = pd.DataFrame({"time": [1, 2, 3], "open": [1, 1, 1], "high": [2, 2, 2],
                          "low": [0, 0, 0], "close": [1, 1, 1]})
    for root in roots:
        frame.to_csv(root / "NQ, 20.csv", index=False)
    out = tmp_path / "catalog.csv"
    monkeypatch.setattr(sys, "argv", ["daedalus", "catalog", *(str(root) for root in roots),
                                      "--output", str(out)])
    assert cli.main() == 0
    report = json.loads(capsys.readouterr().out)
    assert report["real_csv_files"] == 2
    assert report["unique_sha256"] == 1
    assert report["source_roots"] == [str(root) for root in roots]
    catalog = pd.read_csv(out)
    assert len(catalog) == 2
    assert set(catalog["path"]) == {str(root / "NQ, 20.csv") for root in roots}


def test_bridge_forces_research_only_even_with_malicious_candidate_field(tmp_path):
    source = {"experiment_id": "e1", "production_authorized": True}
    path = export_candidate(tmp_path / "candidate.json", source)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["production_authorized"] is False
    assert manifest["candidate"]["production_authorized"] is False
    assert manifest["status"] == "RESEARCH_CANDIDATE_ONLY"
    assert source["production_authorized"] is True
