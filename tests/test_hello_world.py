from fastapi.testclient import TestClient

from journal.hello_world import hello_world
from journal.main import prod_app

client = TestClient(prod_app())


def test_hello_world() -> None:
    assert hello_world() == "Hello, World!"
