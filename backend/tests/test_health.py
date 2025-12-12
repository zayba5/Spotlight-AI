from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_ok():
	"""Basic health check endpoint should return 200 and status ok."""
	resp = client.get("/health")
	assert resp.status_code == 200
	body = resp.json()
	assert body.get("status") == "ok"


