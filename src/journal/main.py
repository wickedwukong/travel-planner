from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
import httpx
from fastapi import FastAPI
from .repository.journal_repository import DBJournalRepository
from pydantic import BaseModel

from .journal import journal_router
from .repository.journal_repository import JournalRepository
import sqlite3
from .repository.migrate_db import DB_PATH
from .weather_client import WeatherAPIClient
import os

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


def factory(journal_repository: JournalRepository, client: WeatherAPIClient) -> FastAPI:
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

    @asynccontextmanager
    async def lifespan(app) -> AsyncGenerator[None, Any]:
        try:
            yield
        finally:
            print("Shutting down...")
            await client.http_client.aclose()
            journal_repository.close()
            print("Shutdown complete.")

    return app


def prod_app() -> FastAPI:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    weather_api_key: str = os.environ["WEATHER_API_KEY"]
    weather_api_client: WeatherAPIClient = WeatherAPIClient(
            api_key=weather_api_key,
            base_url="https://api.weatherapi.com",
            http_client=httpx.AsyncClient()
        )
    return factory(DBJournalRepository(conn), weather_api_client)

