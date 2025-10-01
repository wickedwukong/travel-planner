import sqlite3

from journal.journal import JournalEntryInput
from journal.repository.db_migrator import apply_migrations
from journal.repository.journal_repository import JournalRepository, DBJournalRepository
import os

DB_PATH = "test_journal.db"


def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    apply_migrations(f"sqlite:///{DB_PATH}")


def test_save_journal_entry():
    setup_db()
    conn = sqlite3.connect(DB_PATH)
    db_journal_repository: JournalRepository = DBJournalRepository(conn)
    entry = db_journal_repository.save(
        JournalEntryInput(location="Test Location", note="Test entry")
    )
    assert entry.id is not None
    assert entry.location == "Test Location"
    assert entry.note == "Test entry"
    assert entry.weather is None
    assert entry.created_at is not None
    assert entry.updated_at is None
