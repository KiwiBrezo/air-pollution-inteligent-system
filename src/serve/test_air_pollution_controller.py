from fastapi.testclient import TestClient

from .air_pollution_controller import app

client = TestClient(app)


def test_read_main():
    response = client.get("/air")
    assert response.status_code == 200
