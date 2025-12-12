import json

import pytest

from backend.services import gemini_service


class _FakeResponse:
	def __init__(self, text: str):
		self.text = text


class _FakeModels:
	@staticmethod
	def generate_content(model, contents, config):
		# The actual content/config is not important for the test
		return _FakeResponse(
			'{"use_chroma": true, "use_google_places": true, '
			'"google_places_query": "q", "google_places_location": null, "google_places_radius": 3000}'
		)


class _FakeClient:
	models = _FakeModels()


def test_plan_data_sources_valid(monkeypatch):
	"""Gemini returns valid JSON plan which is parsed and normalized."""

	monkeypatch.setattr(gemini_service, "_get_client", lambda: _FakeClient())

	plan = gemini_service.plan_data_sources("q", None)
	assert plan["use_chroma"] is True
	assert plan["use_google_places"] is True
	assert plan["google_places_query"] == "q"
	assert plan["google_places_radius"] == 3000


def test_plan_data_sources_invalid_json(monkeypatch):
	"""Invalid JSON from Gemini should raise a GeminiServiceError."""

	class _BadModels:
		@staticmethod
		def generate_content(model, contents, config):
			return _FakeResponse("not-json")

	class _BadClient:
		models = _BadModels()

	monkeypatch.setattr(gemini_service, "_get_client", lambda: _BadClient())

	with pytest.raises(gemini_service.GeminiServiceError):
		gemini_service.plan_data_sources("q", None)


