from datetime import datetime
import uuid
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


app = FastAPI()


@app.get("/")
async def home() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None) -> dict:
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict[str, Any]:
    return {"item_id": item_id, "item": item}

