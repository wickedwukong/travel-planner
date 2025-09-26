from hello_world import hello_world
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_hello_world():
    assert hello_world() == "Hello, World!"


def test_update_item():
    pass  # moved to test_update_item.py
