"""Tests for API endpoints."""

from fastapi.testclient import TestClient


def test_root_endpoint():
    """Test root endpoint returns correct response."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "call-audio-pipeline"


def test_health_endpoint():
    """Test health check endpoint."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "call-audio-pipeline"


def test_ready_endpoint():
    """Test readiness check endpoint."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/ready")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["service"] == "call-audio-pipeline"
