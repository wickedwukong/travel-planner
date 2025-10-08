import uuid

from fastapi import APIRouter, HTTPException

from journal.models import JournalEntryInput, JournalEntry
from journal.repository.journal_repository import JournalRepository


def journal_router(journal_repository: JournalRepository) -> APIRouter:
    router = APIRouter()

    @router.post("/journal/entries", status_code=201)
    async def create_travel_journal_entry(
        entry: JournalEntryInput,
    ) -> JournalEntry:
        saved_entry = journal_repository.save(entry)
        return saved_entry

    @router.get("/journal/entries/{entry_id}", status_code=200)
    async def find_journal_entry_by_id(
        entry_id: str,
    ) -> JournalEntry | None:
        entry = journal_repository.find_by_id(uuid.UUID(entry_id))
        if entry is None:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        return entry

    return router
