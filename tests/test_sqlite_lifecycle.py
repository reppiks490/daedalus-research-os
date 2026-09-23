import sqlite3

import pytest

from daedalus.utils import sqlite_connection


def test_sqlite_connection_commits_and_closes(tmp_path):
    path = tmp_path / "lifecycle.sqlite3"
    with sqlite_connection(path) as con:
        con.execute("CREATE TABLE events (id INTEGER)")
        con.execute("INSERT INTO events VALUES (1)")
    with pytest.raises(sqlite3.ProgrammingError):
        con.execute("SELECT 1")
    with sqlite_connection(path) as check:
        assert check.execute("SELECT id FROM events").fetchall() == [(1,)]


def test_sqlite_connection_rolls_back_and_closes(tmp_path):
    path = tmp_path / "rollback.sqlite3"
    with sqlite_connection(path) as con:
        con.execute("CREATE TABLE events (id INTEGER)")
    with pytest.raises(RuntimeError):
        with sqlite_connection(path) as con:
            con.execute("INSERT INTO events VALUES (2)")
            raise RuntimeError("abort")
    with pytest.raises(sqlite3.ProgrammingError):
        con.execute("SELECT 1")
    with sqlite_connection(path) as check:
        assert check.execute("SELECT id FROM events").fetchall() == []
