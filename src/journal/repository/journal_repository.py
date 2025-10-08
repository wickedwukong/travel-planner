import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Protocol, Iterator

from journal.models import JournalEntryInput, JournalEntry


class JournalRepository(Protocol):
    def save(self, entry: JournalEntryInput) -> JournalEntry: ...
    def find_by_id(self, entry_id: uuid.UUID) -> JournalEntry | None: ...
    def close(self) -> None: ...
    def all_entries(self) -> Iterator[JournalEntry]: ...
    def remove_all(self) -> None: ...


class DBJournalRepository(JournalRepository):
    def remove_all(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM journal_entries")
        self.conn.commit()

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
        self.conn.commit()

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

    def all_entries(self) -> Iterator[JournalEntry]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, location, note, created_at FROM journal_entries")
        rows = cursor.fetchall()
        for row in rows:
            yield JournalEntry(
                id=uuid.UUID(row[0]),
                location=row[1],
                note=row[2],
                created_at=datetime.fromisoformat(row[3]),
                weather=None,
                updated_at=None,
            )

    def close(self) -> None:
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
