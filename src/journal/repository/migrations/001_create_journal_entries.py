#
# file: migrations/0001_create_journal_entries.py
#
from yoyo import step

steps = [
    step(
        "CREATE TABLE journal_entries (id TEXT PRIMARY KEY,location TEXT NOT NULL,note TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT)",
        "DROP TABLE journal_entries",
    )
]
