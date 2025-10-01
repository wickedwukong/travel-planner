import uuid
from datetime import datetime, timezone
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
