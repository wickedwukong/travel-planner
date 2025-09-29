from fastapi.testclient import TestClient

from hello_world import hello_world
from main import app

client = TestClient(app)


def test_hello_world():
    assert hello_world() == "Hello, World!"
