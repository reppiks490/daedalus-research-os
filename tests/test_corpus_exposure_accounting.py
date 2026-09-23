from types import SimpleNamespace

import pandas as pd

from daedalus.config import DaedalusConfig
from daedalus.corpus import research_corpus
from daedalus.holdout import HoldoutAssessment, HoldoutLedger


def test_corpus_counts_ledger_exposure_even_if_evaluation_crashes(tmp_path, monkeypatch):
    data = tmp_path / "data"
    data.mkdir()
    source = data / "NQ.csv"
    source.write_text("time,open,high,low,close\n", encoding="utf-8")
    digest = "a" * 64
    catalog = pd.DataFrame([{"path": str(source), "sha256": digest,
                             "symbol_hint": "NQ", "rows": 10000}])
    monkeypatch.setattr("daedalus.corpus.build_catalog", lambda _: catalog)
    monkeypatch.setattr("daedalus.corpus.select_holdout_exposures", lambda reports, cfg:
                        SimpleNamespace(selected_indices=(0,), budget=1, qualified=1,
                                        to_dict=lambda: {"selected_indices": [0]}))
    monkeypatch.setattr("daedalus.corpus.development_rank_key", lambda report: 1.0)

    def research(path, root, cfg, *, data_root, allow_holdout):
        if not allow_holdout:
            return {"status": "development_qualified", "profile": {"sha256": digest}}
        ledger = HoldoutLedger(root / cfg.runtime.holdout_ledger_path)
        ledger.record(HoldoutAssessment(digest, "p", 10, 20, 0, 0, True))
        raise RuntimeError("simulated interruption after protected exposure")

    monkeypatch.setattr("daedalus.corpus.research_file", research)
    report = research_corpus(data, tmp_path, DaedalusConfig())
    assert report["protected_holdouts_exposed"] == 1
    assert report["globally_eligible_candidates"] == 0
    assert report["reports"][0]["status"] == "error"
