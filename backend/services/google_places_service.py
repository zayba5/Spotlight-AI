import os
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv


load_dotenv()


class PlacesConfigError(RuntimeError):
	"""Raised when Google Places configuration (like API key) is missing."""


class PlacesServiceError(RuntimeError):
	"""Raised when Google Places API calls fail."""


def _get_api_key() -> str:
	api_key = os.getenv("GOOGLE_PLACES_API_KEY") or os.getenv("GOOGLE_API_KEY")
	if not api_key:
		raise PlacesConfigError(
			"Google Places API key not configured. "
			"Set GOOGLE_PLACES_API_KEY or GOOGLE_API_KEY in your environment or .env file."
		)
	return api_key


def search_places(
	query: str,
	location: Optional[str] = None,
	radius: int = 5000,
	max_results: int = 20,
) -> List[Dict[str, Any]]:
	"""
	Search for places using Google Places Text Search API.

	- `query`: free-text query like "coffee shops in San Francisco".
	- `location`: optional "lat,lng" string to bias results.
	- `radius`: search radius in meters when `location` is provided.
	- `max_results`: maximum number of results to return (Google may cap lower).
	"""
	if not query or not query.strip():
		return []

	api_key = _get_api_key()

	params: Dict[str, Any] = {
		"query": query,
		"key": api_key,
	}
	if location:
		params["location"] = location
		params["radius"] = radius

	url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

	try:
		with httpx.Client(timeout=10.0) as client:
			resp = client.get(url, params=params)
	except httpx.RequestError as exc:
		raise PlacesServiceError(f"Google Places request failed: {exc}") from exc

	if resp.status_code != 200:
		raise PlacesServiceError(f"Google Places returned HTTP {resp.status_code}: {resp.text}")

	data = resp.json()
	status = data.get("status")
	if status not in {"OK", "ZERO_RESULTS"}:
		# For details on status codes see: https://developers.google.com/maps/documentation/places/web-service/search-text
		raise PlacesServiceError(f"Google Places error status: {status} ({data.get('error_message')})")

	results = data.get("results", [])[:max_results]
	normalized: List[Dict[str, Any]] = []
	for r in results:
		geometry = r.get("geometry", {}) or {}
		location_obj = geometry.get("location", {}) or {}
		normalized.append(
			{
				"place_id": r.get("place_id"),
				"name": r.get("name"),
				"formatted_address": r.get("formatted_address"),
				"rating": r.get("rating"),
				"user_ratings_total": r.get("user_ratings_total"),
				"types": r.get("types") or [],
				"lat": location_obj.get("lat"),
				"lng": location_obj.get("lng"),
			}
		)
	return normalized


