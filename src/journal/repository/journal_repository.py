import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Protocol

from journal.journal import JournalEntryInput, JournalEntry


class JournalRepository(Protocol):
    def save(self, entry: JournalEntryInput) -> JournalEntry: ...
    def find_by_id(self, entry_id: uuid.UUID) -> JournalEntry | None: ...


class DBJournalRepository(JournalRepository):
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def save(self, entry: JournalEntryInput) -> JournalEntry:
        cursor = self.conn.cursor()
        id: uuid.UUID = uuid.uuid4()
        created_at = datetime.now(timezone.utc)
        cursor.execute(
            "INSERT INTO journal_entries (id, location, note, created_at) VALUES (?, ?, ?, ?)",
            (str(id), entry.location, entry.note, created_at.isoformat()),
        )

        return JournalEntry(
            id=id,
            location=entry.location,
            note=entry.note,
            created_at=created_at,
            weather=None,
            updated_at=None,
        )

    def find_by_id(self, entry_id: uuid.UUID) -> JournalEntry | None:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, location, note, created_at FROM journal_entries WHERE id = ?",
            (str(entry_id),),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        return JournalEntry(
            id=uuid.UUID(row[0]),
            location=row[1],
            note=row[2],
            created_at=datetime.fromisoformat(row[3]),
            weather=None,
            updated_at=None,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
