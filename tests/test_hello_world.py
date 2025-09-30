from fastapi.testclient import TestClient

from journal.hello_world import hello_world
from journal.main import app

client = TestClient(app)


def test_hello_world() -> None:
    assert hello_world() == "Hello, World!"
