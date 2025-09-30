import httpx
import pytest
from httpx import ASGITransport

from journal.main import app


@pytest.mark.asyncio
async def test_create_journal_entry():
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/journal/entries",
            json={"location": "Paris", "note": "Visited the Louvre!"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["location"] == "Paris"
        assert data["note"] == "Visited the Louvre!"
        assert data.get("id") is not None
        assert data.get("weather") is None
        assert data.get("created_at") is not None
        assert data.get("updated_at") is None
