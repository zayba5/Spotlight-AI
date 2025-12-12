import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend import main as main_module
from backend.services import google_places_service


client = TestClient(app)


def test_ingest_google_places_missing_key(monkeypatch):
	"""
	If the underlying search_places raises PlacesConfigError (e.g., no API key),
	the endpoint should surface a 503 to the caller.
	"""

	def bad_search(*args, **kwargs):
		raise google_places_service.PlacesConfigError("no key")

	monkeypatch.setattr(main_module, "search_places", bad_search)

	resp = client.post(
		"/ingest_google_places",
		json={"query": "coffee in SF", "location": None, "radius": 5000, "max_results": 5},
	)
	assert resp.status_code == 503
	assert "no key" in resp.text


def test_ingest_google_places_success(monkeypatch):
	"""
	When search_places returns results and embeddings succeed, the endpoint
	should upsert and return the inserted count.
	"""

	def fake_search(query, location=None, radius=5000, max_results=5):
		return [
			{
				"place_id": "g1",
				"name": "Test Cafe",
				"formatted_address": "123 St",
				"rating": 4.5,
				"user_ratings_total": 10,
				"types": ["cafe"],
				"lat": 1.0,
				"lng": 2.0,
			}
		]

	class FakeCollection:
		def __init__(self):
			self.upserts = []

		def upsert(self, ids, documents, metadatas, embeddings):
			self.upserts.append((ids, documents, metadatas, embeddings))

	class FakeClient:
		def __init__(self):
			self.collection = FakeCollection()

		def get_collection(self, name):
			return self.collection

		def create_collection(self, name, metadata=None):
			return self.collection

	# Patch search, chroma client, and embedding
	monkeypatch.setattr(main_module, "search_places", fake_search)
	monkeypatch.setattr(main_module, "get_chroma_client", lambda: FakeClient())
	monkeypatch.setattr(main_module, "get_or_create_collection", lambda client, name="places": client.get_collection(name))

	from backend.services import gemini_service

	monkeypatch.setattr(gemini_service, "get_embedding", lambda text: [0.1, 0.2, 0.3])

	resp = client.post(
		"/ingest_google_places",
		json={"query": "coffee in SF", "location": None, "radius": 5000, "max_results": 5},
	)
	assert resp.status_code == 200
	body = resp.json()
	assert body["inserted"] == 1


