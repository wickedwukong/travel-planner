import os
import sqlite3
import uuid

from journal.models import JournalEntry, Weather
from journal.repository.db_migrator import apply_migrations
from journal.repository.journal_repository import DBJournalRepository

TEST_DB_PATH = "test_journal.db"


def setup_module(module):
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    apply_migrations(f"sqlite:///{TEST_DB_PATH}")


def setup_function(function):
    conn = sqlite3.connect(TEST_DB_PATH)
    with DBJournalRepository(conn) as journal_repository:
        journal_repository.remove_all()


def test_save_journal_entry():
    conn = sqlite3.connect(TEST_DB_PATH)

    with DBJournalRepository(conn) as repo:
        entry = repo.save(
            JournalEntry(
                id=uuid.uuid4(),
                location="Test Location",
                note="Test entry",
                weather=Weather(temperature=25.0, description="Sunny"),
            )
        )

    assert entry.id is not None
    assert entry.location == "Test Location"
    assert entry.note == "Test entry"
    assert entry.weather == Weather(temperature=25.0, description="Sunny")
    assert entry.created_at is not None
    assert entry.updated_at is None


def test_find_journal_entry_by_id():
    conn = sqlite3.connect(TEST_DB_PATH)
    with DBJournalRepository(conn) as repo:
        entry = repo.save(
            JournalEntry(
                id=uuid.uuid4(),
                location="Test Location",
                note="Test entry",
                weather=Weather(temperature=20.0, description="Cloudy"),
            )
        )
        saved_entry = repo.find_by_id(entry.id)

    assert saved_entry == entry


def test_find_all_journal_entries():
    conn = sqlite3.connect(TEST_DB_PATH)
    with DBJournalRepository(conn) as repo:
        entry1 = repo.save(
            JournalEntry(
                id=uuid.uuid4(),
                location="Test Location1",
                note="Test entry1",
                weather=Weather(temperature=22.0, description="Partly Cloudy"),
            )
        )

        entry2 = repo.save(
            JournalEntry(
                id=uuid.uuid4(),
                location="Test Location2",
                note="Test entry2",
                weather=Weather(temperature=30.0, description="Sunny"),
            )
        )

        saved_entries = repo.all_entries()

        assert list(saved_entries) == [entry1, entry2]


def test_remove_all_journal_entries():
    conn = sqlite3.connect(TEST_DB_PATH)
    with DBJournalRepository(conn) as repo:
        repo.save(
            JournalEntry(
                id=uuid.uuid4(),
                location="Test Location1",
                note="Test entry1",
                weather=Weather(temperature=22.0, description="Partly Cloudy"),
            )
        )

        repo.save(
            JournalEntry(
                id=uuid.uuid4(),
                location="Test Location2",
                note="Test entry2",
                weather=Weather(temperature=30.0, description="Sunny"),
            )
        )

        repo.remove_all()
        saved_entries = repo.all_entries()

        assert list(saved_entries) == []
