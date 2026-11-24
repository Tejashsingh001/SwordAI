"""Minimal verification that the shared FastAPI test infrastructure works."""

from fastapi.testclient import TestClient


def test_health_endpoint_uses_isolated_test_client(client: TestClient) -> None:
    """Verify the test client can call the application health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
