from pathlib import Path
import pandas as pd
from daedalus.catalog import build_catalog


def test_exact_duplicates_are_marked_but_distinct_mechanics_preserved(tmp_path: Path):
    a = pd.DataFrame({"time":[1,2,3],"open":[1,1,1],"high":[2,2,2],"low":[0,0,0],"close":[1,1,1]})
    b = pd.DataFrame({"time":[1,1.001,2],"open":[1,1,1],"high":[2,2,2],"low":[0,0,0],"close":[1,1,1]})
    a.to_csv(tmp_path/"X, 1.csv",index=False)
    a.to_csv(tmp_path/"X, 1 2.csv",index=False)
    b.to_csv(tmp_path/"X, 1 3.csv",index=False)
    cat = build_catalog(tmp_path)
    assert len(cat)==3
    assert cat.sha256.nunique()==2
    assert cat.mechanics_signature.nunique()==2


def test_multiple_roots_preserve_distinct_files_without_double_scanning_overlap(tmp_path: Path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    frame = pd.DataFrame({"time": [1, 2], "open": [1, 1], "high": [2, 2],
                          "low": [0, 0], "close": [1, 1]})
    frame.to_csv(a / "NQ, 20.csv", index=False)
    frame.to_csv(b / "NQ, 20.csv", index=False)
    cat = build_catalog([a, b, a])
    assert len(cat) == 2
    assert cat.sha256.nunique() == 1
    assert set(cat.exact_duplicate_count) == {2}
    assert len(set(cat.path)) == 2


def test_catalog_rejects_missing_root(tmp_path: Path):
    import pytest

    with pytest.raises(ValueError, match="not a directory"):
        build_catalog([tmp_path / "missing"])
