import sqlite3
import uuid
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException

from journal.models import JournalEntryInput, JournalEntry, Weather
from journal.repository.journal_repository import DBJournalRepository
from journal.repository.migrate_db import DB_PATH


def get_db_journal_repository() -> Generator[DBJournalRepository, None, None]:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield DBJournalRepository(conn)
    finally:
        conn.close()


def journal_router(journal_repository: JournalEntry) -> APIRouter:
    router = APIRouter()

    @router.post("/journal/entries", status_code=201)
    async def create_travel_journal_entry(
        entry: JournalEntryInput,
        db_journal_repository: DBJournalRepository = Depends(get_db_journal_repository),
    ) -> JournalEntry:
        saved_entry = db_journal_repository.save(entry)
        return saved_entry

    @router.get("/journal/entries/{entry_id}", status_code=200)
    async def find_journal_entry_by_id(
        entry_id: str,
        db_journal_repository: DBJournalRepository = Depends(get_db_journal_repository),
    ) -> JournalEntry | None:
        entry = db_journal_repository.find_by_id(uuid.UUID(entry_id))
        if entry is None:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        return entry

    return router
