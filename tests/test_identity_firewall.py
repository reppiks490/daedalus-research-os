import csv

import pytest

from daedalus.identity import load_identity_manifest, resolve_identity


def _manifest(path, rows):
    columns = ["relative_path", "canonical_symbol", "chart_type",
               "representation_role", "execution_safe", "notes"]
    with path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _row(path):
    return {"relative_path": path, "canonical_symbol": "NQ", "chart_type": "clock_minutes",
            "representation_role": "execution", "execution_safe": "true", "notes": "reviewed"}


def test_duplicate_manifest_identity_fails_instead_of_overwriting(tmp_path):
    manifest = tmp_path / "identities.csv"
    _manifest(manifest, [_row("a/NQ.csv"), _row("a\\NQ.csv")])
    with pytest.raises(ValueError, match="Duplicate source identity"):
        load_identity_manifest(manifest)


@pytest.mark.parametrize("name", ["../NQ.csv", "/NQ.csv", "C:/NQ.csv", ""])
def test_manifest_rejects_paths_outside_the_source_root(tmp_path, name):
    manifest = tmp_path / "identities.csv"
    _manifest(manifest, [_row(name)])
    with pytest.raises(ValueError, match="Invalid source identity"):
        load_identity_manifest(manifest)


def test_external_same_named_file_cannot_inherit_execution_safe_identity(tmp_path):
    root = tmp_path / "clock"
    other = tmp_path / "renko"
    root.mkdir()
    other.mkdir()
    source = other / "NQ.csv"
    source.write_text("time,open,high,low,close\n", encoding="utf-8")
    manifest = tmp_path / "identities.csv"
    _manifest(manifest, [_row("NQ.csv")])
    with pytest.raises(ValueError, match="outside its declared data root"):
        resolve_identity(source, root, load_identity_manifest(manifest), "NQ")
