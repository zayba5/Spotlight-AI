import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend import main as main_module
from backend.services import gemini_service


client = TestClient(app)


def test_chat_empty_query():
	"""Empty query text should be rejected with 400."""
	resp = client.post(
		"/chat",
		json={
			"user_id": "u1",
			"query": "   ",
			"location_hint": None,
			"update_preferences": None,
			"conversation_id": None,
		},
	)
	assert resp.status_code == 400
	assert "Query text is required" in resp.text


def test_chat_embedding_empty(monkeypatch):
	"""
	If get_embedding returns an empty vector, the API should return 400
	with an appropriate message.
	"""

	# Avoid real routing; force chroma-only
	monkeypatch.setattr(
		main_module,
		"plan_data_sources",
		lambda query, location_hint=None: {
			"use_chroma": True,
			"use_google_places": False,
			"google_places_query": query,
			"google_places_location": location_hint,
			"google_places_radius": 5000,
		},
	)

	monkeypatch.setattr(main_module, "get_embedding", lambda text: [])

	# Stub out DB-related calls to avoid hitting a real database
	class FakeDB:
		def add(self, *args, **kwargs):
			...

		def commit(self):
			...

		def refresh(self, obj):
			# Mimic SQLAlchemy setting a primary key on refresh so conversation_id is not None
			if getattr(obj, "id", None) is None:
				setattr(obj, "id", 1)

	def fake_get_db():
		return FakeDB()

	main_module.app.dependency_overrides[main_module.get_db] = fake_get_db

	monkeypatch.setattr(
		main_module,
		"get_or_create_user",
		lambda db, external_user_id, display_name=None: type("User", (), {"id": 1})(),
	)
	monkeypatch.setattr(main_module, "set_user_preferences", lambda db, uid, prefs: None)
	monkeypatch.setattr(main_module, "get_user_preferences", lambda db, uid: {})

	resp = client.post(
		"/chat",
		json={
			"user_id": "u1",
			"query": "valid",
			"location_hint": None,
			"update_preferences": None,
			"conversation_id": None,
		},
	)

	assert resp.status_code == 400
	assert "Unable to generate embedding" in resp.text

	# Clean up override
	main_module.app.dependency_overrides.pop(main_module.get_db, None)


def test_chat_routing_plan_failure_falls_back_to_chroma(monkeypatch):
	"""
	If plan_data_sources raises a GeminiServiceError, the code should fall back
	to using Chroma only and still return a successful response.
	"""

	def bad_plan(*args, **kwargs):
		raise gemini_service.GeminiServiceError("routing failed")

	monkeypatch.setattr(main_module, "plan_data_sources", bad_plan)

	# Fake embedding and chroma query
	monkeypatch.setattr(main_module, "get_embedding", lambda text: [0.1, 0.2, 0.3])

	class FakeCollection:
		def query(self, query_embeddings, n_results):
			return {
				"ids": [["id1"]],
				"documents": [["doc"]],
				"metadatas": [[{"title": "src"}]],
			}

	class FakeClient:
		def __init__(self):
			self.collection = FakeCollection()

		def get_collection(self, name):
			return self.collection

		def create_collection(self, name, metadata=None):
			return self.collection

	monkeypatch.setattr(main_module, "get_chroma_client", lambda: FakeClient())
	monkeypatch.setattr(main_module, "get_or_create_collection", lambda client, name="places": client.get_collection(name))

	# Stub DB interactions
	class FakeDB:
		def add(self, *args, **kwargs): ...
		def commit(self): ...
		def refresh(self, obj): ...

	def fake_get_db():
		return FakeDB()

	main_module.app.dependency_overrides[main_module.get_db] = fake_get_db
	monkeypatch.setattr(
		main_module,
		"get_or_create_user",
		lambda db, external_user_id, display_name=None: type("User", (), {"id": 1})(),
	)
	monkeypatch.setattr(main_module, "set_user_preferences", lambda db, uid, prefs: None)
	monkeypatch.setattr(main_module, "get_user_preferences", lambda db, uid: {})

	# Avoid hitting real Gemini for text generation
	monkeypatch.setattr(
		gemini_service,
		"generate_response",
		lambda system_prompt, user_prompt: "fallback answer",
	)

	resp = client.post(
		"/chat",
		json={
			"user_id": "u1",
			"query": "something",
			"location_hint": None,
			"update_preferences": None,
			"conversation_id": None,
		},
	)

	assert resp.status_code == 200
	data = resp.json()
	assert data["answer"] == "fallback answer"

	# Clean up override
	main_module.app.dependency_overrides.pop(main_module.get_db, None)


