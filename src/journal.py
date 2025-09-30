from datetime import datetime, timezone
import uuid
from fastapi import APIRouter
from pydantic import BaseModel

class Weather(BaseModel):
    description: str
    temperature: float

class JournalEntryInput(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    location: str
    note: str

class JournalEntry(JournalEntryInput):
    weather: Weather | None = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime | None = None

router = APIRouter()

@router.post("/journal/entries", status_code=201)
async def create_travel_journal_entry(entry: JournalEntryInput) -> JournalEntry:
    return JournalEntry(**entry.model_dump(), weather=None)

