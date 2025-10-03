from typing import Any
from datetime import datetime

from fastapi import FastAPI
from journal.repository.journal_repository import DBJournalRepository
from pydantic import BaseModel

from journal.journal import journal_router
from journal.repository.journal_repository import JournalRepository
import sqlite3
from journal.repository.migrate_db import DB_PATH


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


def factory(journal_repository: JournalRepository) -> FastAPI:
    app = FastAPI()
    app.include_router(journal_router(journal_repository))

    @app.get("/")
    async def home() -> dict[str, str]:
        return {"message": "Hello, World!"}

    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: str | None = None) -> dict:
        return {"item_id": item_id, "q": q}

    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: Item) -> dict[str, Any]:
        return {"item_id": item_id, "item": item}

    return app


def prod_app() -> FastAPI:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return factory(DBJournalRepository(conn))
