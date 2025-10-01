import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Protocol

from journal.journal import JournalEntryInput, JournalEntry


class JournalRepository(Protocol):
    def save(self, entry: JournalEntryInput) -> JournalEntry: ...


class DBJournalRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def save(self, entry: JournalEntryInput) -> JournalEntry:
        cursor = self.conn.cursor()
        id: str = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO journal_entries (id, location, note, created_at) VALUES (?, ?, ?, ?)",
            (id, entry.location, entry.note, datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()
        cursor.execute(
            "SELECT id, location, note, created_at FROM journal_entries WHERE id = ?",
            (id,),
        )
        row = cursor.fetchone()
        return JournalEntry(
            id=uuid.UUID(row[0]),
            location=row[1],
            note=row[2],
            created_at=datetime.fromisoformat(row[3]),
            weather=None,
            updated_at=None,
        )
