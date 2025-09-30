import httpx
import pytest
from httpx import ASGITransport

from main import app


@pytest.mark.asyncio
async def test_create_journal_entry():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/journal/entries", json={
            "city": "Paris",
            "note": "Visited the Louvre!"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["city"] == "Paris"
        assert data["note"] == "Visited the Louvre!"
        assert "id" in data
        assert "weather" in data
        assert "created_at" in data
