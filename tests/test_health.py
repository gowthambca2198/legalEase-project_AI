from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"

    assert data["name"] == "LegalEase"


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert "gemini_configured" in data

    assert "demo_mode" in data