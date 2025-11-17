import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

GEMINI_GENERATE_MODEL = os.getenv("GEMINI_GENERATE_MODEL") or os.getenv("GEMINI_MODEL") or "gemini-2.5-pro"
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL") or "text-embedding-004"

class GeminiServiceError(RuntimeError):
	"""Base exception for Gemini-related failures."""


class GeminiConfigError(GeminiServiceError):
	"""Raised when Gemini configuration (like API key) is missing."""

client = genai.Client()


def _ensure_text_from_response(response: Any) -> str:
	if hasattr(response, "output_text") and response.output_text:
		return response.output_text

	if hasattr(response, "text") and response.text:
		return response.text

	# Some responses may return candidates with content parts
	if hasattr(response, "candidates") and response.candidates:
		for candidate in response.candidates:
			if hasattr(candidate, "content") and getattr(candidate.content, "parts", None):
				parts = candidate.content.parts
				text_parts = [getattr(part, "text", "") for part in parts if getattr(part, "text", "")]
				if text_parts:
					return "\n".join(text_parts)

	# Dict fallback
	if isinstance(response, dict):
		if "text" in response and response["text"]:
			return response["text"]
		candidates = response.get("candidates") or []
		for cand in candidates:
			parts = cand.get("content", {}).get("parts", [])
			text_parts = [part.get("text") for part in parts if part.get("text")]
			if text_parts:
				return "\n".join(text_parts)

	return ""


def _ensure_embedding_from_response(response: Any) -> List[float]:
	# API may return .embedding (single) or .embeddings (list)
	if hasattr(response, "embedding") and response.embedding:
		embedding = getattr(response.embedding, "values", response.embedding)
		return list(embedding)

	if hasattr(response, "embeddings") and response.embeddings:
		first = response.embeddings[0]
		if hasattr(first, "values"):
			return list(first.values)
		return list(first)

	if hasattr(response, "data") and response.data:
		return list(response.data)

	if isinstance(response, dict):
		if "embedding" in response:
			embedding_obj = response["embedding"]
			if isinstance(embedding_obj, dict) and "values" in embedding_obj:
				return list(embedding_obj["values"])
			return list(embedding_obj)
		if "embeddings" in response and response["embeddings"]:
			first = response["embeddings"][0]
			if isinstance(first, dict):
				if "values" in first:
					return list(first["values"])
				if "embedding" in first and isinstance(first["embedding"], dict):
					return list(first["embedding"].get("values", []))
		if "data" in response and response["data"]:
			first = response["data"][0]
			if isinstance(first, dict):
				if "embedding" in first and isinstance(first["embedding"], dict):
					return list(first["embedding"].get("values", []))
				if "values" in first:
					return list(first["values"])

	raise GeminiServiceError("Gemini response did not include an embedding vector.")


def get_embedding(text: str) -> List[float]:
	if not text:
		return []
	try:
		response = client.models.embed_content(
			model=GEMINI_EMBED_MODEL,
			contents={"parts": [{"text": text}]},
		)
		client.close()
	except TypeError:
		response = client.models.embed_content(
			model=GEMINI_EMBED_MODEL,
			contents=text,
		)
		client.close()
	except Exception as exc:  # pragma: no cover - SDK specific errors
		raise GeminiServiceError(f"Gemini embedding request failed: {exc}") from exc
	return _ensure_embedding_from_response(response)


@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
def generate_response(system_prompt: str, user_prompt: str) -> str:
	try:
		response = client.models.generate_content(
			model=GEMINI_GENERATE_MODEL,
			system_instruction=system_prompt,
			contents=user_prompt,
		)
		client.close()
	except Exception as exc:  # pragma: no cover - SDK specific errors
		raise GeminiServiceError(f"Gemini text generation failed: {exc}") from exc

	text = _ensure_text_from_response(response).strip()
	if not text:
		raise GeminiServiceError("Gemini returned an empty response.")
	return text


def build_system_prompt(preference_summary: str) -> str:
	return (
		"You are Spotlight-AI, a local recommendations assistant. You answer with concise, clear suggestions "
		"based on retrieved reviews, menus, and ratings. Always include relevant citations as [n] referencing items provided. "
		f"Personalization context: {preference_summary or 'none'}"
	)


def build_user_prompt(query: str, retrieved: List[Dict[str, Any]]) -> str:
	# Format retrieved chunks with numeric indices for citations
	lines = ["User question: " + query.strip(), "", "Retrieved context:"]
	if not retrieved:
		lines.append("[1] No documents retrieved. Provide best-effort answer based on general knowledge and preferences.")
	else:
		for i, item in enumerate(retrieved, start=1):
			metadata = item.get("metadata", {}) or {}
			title = metadata.get("title") or metadata.get("name") or "Source"
			url = metadata.get("url") or ""
			snippet = (item.get("document") or "")[:1200]
			lines.append(f"[{i}] {title} {url}\n{snippet}")
	lines.append("")
	lines.append(
		"Instructions: Provide top 3-5 recommendations if applicable. Use citations like [1], [2]. "
		"Prioritize the user's preferences. Be specific about quietness, vegetarian options, budget, and distance when available."
	)
	return "\n".join(lines)
