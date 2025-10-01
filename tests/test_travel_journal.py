import httpx
import pytest
from httpx import ASGITransport

from journal.main import prod_app

@pytest.mark.asyncio
async def test_create_journal_entry():
    async with httpx.AsyncClient(
        transport=ASGITransport(app=prod_app()), base_url="http://test"
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

@pytest.mark.asyncio
async def test_find_journal_entry_by_id():
    async with httpx.AsyncClient(
        transport=ASGITransport(app=prod_app()), base_url="http://test"
    ) as client:
        create_response = await client.post(
            "/journal/entries",
            json={"location": "Paris", "note": "Visited the Louvre!"},
        )

        created_entry = create_response.json()
        entry_id = created_entry["id"]

        fetch_response = await client.get(f"/journal/entries/{entry_id}")
        assert fetch_response.status_code == 200
        fetched_entry = fetch_response.json()
        assert fetched_entry == created_entry
