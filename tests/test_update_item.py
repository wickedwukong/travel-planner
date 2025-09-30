from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_update_item():
    item_id = 1
    payload = {
        "name": "Test Item",
        "price": 9.99,
        "is_offer": True,
    }
    response = client.put(f"/items/{item_id}", json=payload)
    assert response.status_code == 200
    data: dict = response.json()
    assert data["item_id"] == item_id
    assert data["item"] == payload
