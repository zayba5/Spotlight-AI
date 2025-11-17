import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import google.genai as genai
from tenacity import retry, wait_exponential, stop_after_attempt

load_dotenv()

GEMINI_GENERATE_MODEL = os.getenv("GEMINI_GENERATE_MODEL")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
	raise RuntimeError("GEMINI_API_KEY is not set. Please configure it in your environment.")

client = genai.Client(api_key=GEMINI_API_KEY)


def get_embedding(text: str) -> List[float]:
	if not text:
		return []
	resp = client.models.embed_content(model=GEMINI_EMBED_MODEL, content=text)
	return resp["embedding"]


@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
def generate_response(system_prompt: str, user_prompt: str) -> str:
	resp = client.models.generate_content(
		model=GEMINI_GENERATE_MODEL,
		contents=[user_prompt],
		system_instruction=system_prompt,
	)
	return resp.text or ""


def build_system_prompt(preference_summary: str) -> str:
	return (
		"You are Spotlight-AI, a local recommendations assistant. You answer with concise, clear suggestions "
		"based on retrieved reviews, menus, and ratings. Always include relevant citations as [n] referencing items provided. "
		f"Personalization context: {preference_summary or 'none'}"
	)


def build_user_prompt(query: str, retrieved: List[Dict[str, Any]]) -> str:
	# Format retrieved chunks with numeric indices for citations
	lines = ["User question: " + query, "", "Retrieved context:"]
	for i, item in enumerate(retrieved, start=1):
		title = item.get("metadata", {}).get("title") or item.get("metadata", {}).get("name") or "Source"
		url = item.get("metadata", {}).get("url") or ""
		snippet = item.get("document", "")[:1200]
		lines.append(f"[{i}] {title} {url}\n{snippet}")
	lines.append("")
	lines.append("Instructions: Provide top 3-5 recommendations if applicable. Use citations like [1], [2]. "
				 "Prioritize user's preferences. Be specific about quietness, vegetarian, budget, and distance when available.")
	return "\n".join(lines)



