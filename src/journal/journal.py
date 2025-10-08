import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from .models import JournalEntryInput, JournalEntry
from .repository.journal_repository import JournalRepository
from .weather_client import WeatherAPIClient

def journal_router(
    journal_repository: JournalRepository, client: WeatherAPIClient
) -> APIRouter:
    router = APIRouter()

    @router.post("/journal/entries", status_code=201)
    async def create_travel_journal_entry(
        entry: JournalEntryInput,
    ) -> JournalEntry:
        weather = await client.weather(entry.location)
        entry = JournalEntry(
            id=uuid.uuid4(),
            location=entry.location, note=entry.note, weather=weather
        )
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

    @router.get("/journal/entries", status_code=200, response_model=None)
    async def all_journal_entries():
        def entry_stream():
            yield "["
            first = True
            for entry in journal_repository.all_entries():
                if not first:
                    yield ","
                else:
                    first = False

                yield entry.model_dump_json()

            yield "]"


        return StreamingResponse(entry_stream(), media_type="application/json")

    return router
