import csv

import pandas as pd
import pytest

from daedalus.config import DaedalusConfig
from daedalus.corpus import research_corpus


def test_exact_byte_copies_with_conflicting_chart_identities_block_corpus(tmp_path, monkeypatch):
    data = tmp_path / "data"
    data.mkdir()
    frame = pd.DataFrame({"time": [1, 2, 3], "open": [1, 1, 1], "high": [2, 2, 2],
                          "low": [0, 0, 0], "close": [1, 1, 1]})
    for name in ("clock.csv", "renko.csv"):
        frame.to_csv(data / name, index=False)
    config = tmp_path / "config"
    config.mkdir()
    manifest = config / "source_identity.csv"
    columns = ["relative_path", "canonical_symbol", "chart_type",
               "representation_role", "execution_safe", "notes"]
    with manifest.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        writer.writerow(dict(zip(columns, ["clock.csv", "NQ", "clock_minutes", "execution", "true", ""])))
        writer.writerow(dict(zip(columns, ["renko.csv", "NQ", "renko", "representation", "false", ""])))

    def should_not_research(*args, **kwargs):
        raise AssertionError("protected or development research started")

    monkeypatch.setattr("daedalus.corpus.research_file", should_not_research)
    with pytest.raises(ValueError, match="disagree on chart identity"):
        research_corpus(data, tmp_path, DaedalusConfig())
    assert not (tmp_path / "artifacts" / "corpus_research_summary.json").exists()
