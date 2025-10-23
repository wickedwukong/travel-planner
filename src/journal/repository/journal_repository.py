import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Iterator, Protocol

from journal.models import JournalEntry, Weather


class JournalRepository(Protocol):
    def save(self, entry: JournalEntry) -> JournalEntry: ...
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

    def save(self, entry: JournalEntry) -> JournalEntry:
        cursor = self.conn.cursor()
        created_at = datetime.now(timezone.utc)
        cursor.execute(
            "INSERT INTO journal_entries (id, location, note, temperature, description, created_at) VALUES (?,?,?, ?, ?, ?)",
            (
                str(entry.id),
                entry.location,
                entry.note,
                entry.weather.temperature,
                entry.weather.description,
                created_at.isoformat(),
            ),
        )
        self.conn.commit()

        return self.find_by_id(entry.id)

    def find_by_id(self, entry_id: uuid.UUID) -> JournalEntry | None:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, location, note, temperature, description, created_at, updated_at FROM journal_entries WHERE id = ?",
            (str(entry_id),),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        return JournalEntry(
            id=uuid.UUID(row[0]),
            location=row[1],
            note=row[2],
            weather=Weather(temperature=float(row[3]), description=row[4]),
            created_at=datetime.fromisoformat(row[5]),
            updated_at=datetime.fromisoformat(row[6]) if row[6] else None,
        )

    def all_entries(self) -> Iterator[JournalEntry]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, location, note, temperature, description, created_at, updated_at FROM journal_entries"
        )
        rows = cursor.fetchall()
        for row in rows:
            yield JournalEntry(
                id=uuid.UUID(row[0]),
                location=row[1],
                note=row[2],
                weather=Weather(temperature=float(row[3]), description=row[4]),
                created_at=datetime.fromisoformat(row[5]),
                updated_at=datetime.fromisoformat(row[6]) if row[6] else None,
            )

    def close(self) -> None:
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
