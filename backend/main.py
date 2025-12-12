import os
import random
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.chroma_utils import get_chroma_client, get_or_create_collection
from backend.database import models
from backend.database.db import Base, engine, get_db
from backend.services.data_ingest_service import ingest_businesses_from_db
from backend.services.google_places_service import (
	PlacesConfigError,
	PlacesServiceError,
	search_places,
)
from backend.services.gemini_service import (
	GeminiConfigError,
	GeminiServiceError,
	build_system_prompt,
	build_user_prompt,
	generate_response,
	get_embedding,
	plan_data_sources,
)
from backend.services.memory_service import (
	get_or_create_user,
	get_user_preferences,
	set_user_preferences,
	summarize_preferences,
)

load_dotenv()

default_origins = [
	"http://localhost:8501",
	"http://127.0.0.1:8501",
	"http://localhost:3000",
]
extra_origins = [
	origin.strip()
	for origin in os.getenv("CORS_ALLOW_ORIGINS", "").split(",")
	if origin.strip()
]
ALLOW_ORIGINS = list({origin for origin in default_origins + extra_origins})

# Initialize DB schema if not exists
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spotlight-AI Backend", version="0.1.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=ALLOW_ORIGINS or ["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


class HealthResponse(BaseModel):
	status: str = "ok"


class IngestItem(BaseModel):
	id: str = Field(..., description="Unique id for the document")
	title: Optional[str] = None
	url: Optional[str] = None
	location: Optional[str] = None
	tags: Optional[List[str]] = None
	text: str


class IngestRequest(BaseModel):
	items: List[IngestItem]


class GooglePlacesIngestRequest(BaseModel):
	query: str = Field(..., description="Free-text query, e.g. 'coffee shops in San Francisco'")
	location: Optional[str] = Field(
		None,
		description="Optional 'lat,lng' string to bias results, e.g. '37.7749,-122.4194'",
	)
	radius: int = Field(
		5000,
		ge=1,
		le=50000,
		description="Search radius in meters when location is provided.",
	)
	max_results: int = Field(
		20,
		ge=1,
		le=50,
		description="Maximum number of places to ingest from Google Places.",
	)


class ChatRequest(BaseModel):
	user_id: str
	query: str
	# Optional human-readable location hint (city / neighborhood)
	location_hint: Optional[str] = None
	# Optional precise location; if both latitude and longitude are provided,
	# they will be used to bias nearby restaurant searches (e.g. Google Places).
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	update_preferences: Optional[Dict[str, str]] = None
	conversation_id: Optional[int] = None
	# Optional structured filters coming from the frontend UI (price, distance, etc.).
	filters: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
	answer: str
	citations: List[Dict[str, Any]] = []
	conversation_id: int


@app.get("/health", response_model=HealthResponse)
def health():
	return HealthResponse()


@app.post("/ingest")
def ingest(req: IngestRequest):
	if not req.items:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No items provided for ingestion.")

	client = get_chroma_client()
	col = get_or_create_collection(client)

	ids = [it.id for it in req.items]
	documents = [it.text for it in req.items]
	metadatas = []
	embeddings = []
	for it in req.items:
		metadatas.append(
			{
				"title": it.title,
				"url": it.url,
				"location": it.location,
				"tags": ", ".join(it.tags) if it.tags else None,
			}
		)
		try:
			embeddings.append(get_embedding(it.text))
		except GeminiConfigError as exc:
			raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
		except GeminiServiceError as exc:
			raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
		except Exception as exc:  # pragma: no cover - unexpected failures
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Embedding generation failed.") from exc

	col.upsert(ids=ids, metadatas=metadatas, documents=documents, embeddings=embeddings)
	return {"inserted": len(ids)}


@app.post("/ingest_google_places")
def ingest_google_places(req: GooglePlacesIngestRequest):
	"""
	Fetch places from Google Places Text Search API and ingest them into the Chroma collection.

	Each place is turned into a short descriptive document and embedded with Gemini, then upserted into
	the same Chroma collection used for other content. IDs are prefixed with 'gplace_'.
	"""
	try:
		places = search_places(
			query=req.query,
			location=req.location,
			radius=req.radius,
			max_results=req.max_results,
		)
	except PlacesConfigError as exc:
		raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
	except PlacesServiceError as exc:
		raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

	if not places:
		return {"inserted": 0}

	client = get_chroma_client()
	col = get_or_create_collection(client)

	ids: List[str] = []
	documents: List[str] = []
	metadatas: List[Dict[str, Any]] = []
	embeddings: List[List[float]] = []

	for p in places:
		place_id = p.get("place_id")
		if not place_id:
			continue
		ids.append(f"gplace_{place_id}")

		name = p.get("name") or "Place"
		addr = p.get("formatted_address") or ""
		rating = p.get("rating")
		rating_count = p.get("user_ratings_total") or 0
		types = p.get("types") or []

		base_desc = f"{name} located at {addr}. "
		type_str = ", ".join(types)
		if type_str:
			base_desc += f"Types: {type_str}. "
		if rating is not None:
			base_desc += f"Rating: {rating} based on {rating_count} Google reviews. "

		documents.append(base_desc.strip())
		metadatas.append(
			{
				"title": name,
				"address": addr,
				"rating": rating,
				"review_count": rating_count,
				"types": type_str,
				"source": "google_places",
				"place_id": place_id,
				"lat": p.get("lat"),
				"lng": p.get("lng"),
			}
		)
		try:
			embeddings.append(get_embedding(base_desc))
		except GeminiConfigError as exc:
			raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
		except GeminiServiceError as exc:
			raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
		except Exception as exc:  # pragma: no cover - unexpected failures
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Embedding generation failed.") from exc

	if ids:
		col.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

	return {"inserted": len(ids)}


@app.post("/ingest_db")
def ingest_db(
	db: Session = Depends(get_db),
	max_rows: Optional[int] = Query(
		None,
		ge=1,
		description="Maximum number of businesses to ingest from the database.",
	),
	min_review_count: Optional[int] = Query(
		None,
		ge=0,
		description="Only ingest businesses with at least this many reviews.",
	),
	city: Optional[str] = Query(
		None,
		description="Only ingest businesses in this exact city (matches `Business.city`).",
	),
	batch_size: int = Query(
		100,
		ge=1,
		le=1000,
		description="Number of businesses to embed and upsert per batch.",
	),
):
	"""
	Ingest data from the Postgres `data` schema into ChromaDB.

	Uses the `data.businesses` and `data.reviews` tables via `Business` / `Review` models,
	with optional filters and batching for performance.
	"""
	count = ingest_businesses_from_db(
		db,
		max_rows=max_rows,
		min_review_count=min_review_count,
		city=city,
		batch_size=batch_size,
	)
	return {"inserted": count}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
	if not req.query or not req.query.strip():
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query text is required.")

	# Ensure user record and update long‑term preferences if provided
	user = get_or_create_user(db, external_user_id=req.user_id)
	if req.update_preferences:
		set_user_preferences(db, user.id, req.update_preferences)
	prefs = get_user_preferences(db, user.id)
	pref_summary = summarize_preferences(prefs)

	# Short-lived, request-scoped filters from the frontend (price range, distance, etc.).
	active_filters: Dict[str, Any] = req.filters or {}

	def _summarize_filters(filters: Dict[str, Any]) -> str:
		if not filters:
			return "None."
		parts = []
		if "distance_miles" in filters and filters.get("distance_miles") is not None:
			parts.append(f"distance ≤ {filters['distance_miles']} miles")
		if "price_range" in filters and filters.get("price_range"):
			parts.append(f"price range {filters['price_range']}")
		if "dietary" in filters and filters.get("dietary"):
			parts.append(f"dietary: {filters['dietary']}")
		if "noise_preference" in filters and filters.get("noise_preference"):
			parts.append(f"noise: {filters['noise_preference']}")
		if "open_now" in filters:
			parts.append("open now only" if filters["open_now"] else "include closed places")
		return "; ".join(str(p) for p in parts) or "None."

	filter_summary = _summarize_filters(active_filters)

	# Derive a precise "lat,lng" string if available for downstream services
	lat_lng_str: Optional[str] = None
	if req.latitude is not None and req.longitude is not None:
		lat_lng_str = f"{req.latitude},{req.longitude}"

	# Decide which data sources to use (Chroma vs Google Places)
	try:
		plan = plan_data_sources(req.query, lat_lng_str or req.location_hint, active_filters)
	except GeminiServiceError:
		# Fallback: always use Chroma only
		plan = {
			"use_chroma": True,
			"use_google_places": False,
			"google_places_query": req.query,
			"google_places_location": req.location_hint,
			"google_places_radius": 5000,
		}

	retrieved_items: List[Dict[str, Any]] = []

	# Build a human-readable filter text to bias both Google Places and Chroma retrieval.
	filter_text_parts = []
	if active_filters.get("open_now"):
		filter_text_parts.append("open now")
	if active_filters.get("price_range"):
		filter_text_parts.append(f"price range {active_filters['price_range']}")
	if active_filters.get("dietary"):
		filter_text_parts.append(f"dietary preferences {active_filters['dietary']}")
	if active_filters.get("noise_preference"):
		filter_text_parts.append(f"noise level {active_filters['noise_preference']}")
	filter_hint = ", ".join(str(p) for p in filter_text_parts)

	# Optionally query live Google Places results *first* (prioritized over Postgres/Chroma).
	if plan.get("use_google_places"):
		try:
			# Build a slightly enriched query string that bakes in active filters.
			google_query = plan.get("google_places_query") or req.query
			if filter_hint:
				google_query = f"{google_query} ({filter_hint})"

			# Prefer an explicit distance from the frontend filters when available.
			radius_meters: int = int(plan.get("google_places_radius") or 5000)
			if "distance_miles" in active_filters and active_filters["distance_miles"]:
				try:
					radius_meters = int(float(active_filters["distance_miles"]) * 1609.34)
				except (TypeError, ValueError):
					# Ignore bad client-provided values and fall back to the planned radius.
					radius_meters = int(plan.get("google_places_radius") or 5000)

			places = search_places(
				query=google_query,
				location=plan.get("google_places_location") or lat_lng_str or req.location_hint,
				radius=max(1, min(50000, radius_meters)),
				max_results=10,
			)
		except PlacesConfigError as exc:
			raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
		except PlacesServiceError as exc:
			raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

		for p in places:
			place_id = p.get("place_id")
			if not place_id:
				continue

			name = p.get("name") or "Place"
			addr = p.get("formatted_address") or ""
			rating = p.get("rating")
			rating_count = p.get("user_ratings_total") or 0
			types = p.get("types") or []

			base_desc = f"{name} located at {addr}. "
			type_str = ", ".join(types)
			if type_str:
				base_desc += f"Types: {type_str}. "
			if rating is not None:
				base_desc += f"Rating: {rating} based on {rating_count} Google reviews. "

			metadata = {
				"title": name,
				"address": addr,
				"rating": rating,
				"review_count": rating_count,
				"types": type_str,
				"source": "google_places_live",
				"place_id": place_id,
				"lat": p.get("lat"),
				"lng": p.get("lng"),
			}

			retrieved_items.append(
				{
					"id": f"gplace_live_{place_id}",
					"document": base_desc.strip(),
					"metadata": metadata,
				}
			)

	# Retrieve from Chroma (Postgres/embeddings) if requested by the routing plan,
	# after live Google Places, so that live data is prioritized.
	if plan.get("use_chroma", True):
		client = get_chroma_client()
		col = get_or_create_collection(client)
		try:
			# location_hint is used only to slightly bias semantic retrieval; prefer human-readable hints
			location_text = req.location_hint or ""
			query_text = req.query
			if location_text:
				query_text += f" near {location_text}"
			if filter_hint:
				query_text += f" with filters: {filter_hint}"

			query_embedding = get_embedding(query_text)
		except GeminiConfigError as exc:
			raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
		except GeminiServiceError as exc:
			raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

		if not query_embedding:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Unable to generate embedding for the provided query.",
			)

		try:
			results = col.query(query_embeddings=[query_embedding], n_results=8)
		except Exception as exc:  # pragma: no cover - chroma internal failure
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Vector search failed.") from exc

		if results and results.get("ids"):
			for i in range(len(results["ids"][0])):
				item = {
					"id": results["ids"][0][i],
					"document": results["documents"][0][i],
					"metadata": results["metadatas"][0][i],
				}
				retrieved_items.append(item)

	# Build prompt and call Gemini
	system_prompt = build_system_prompt(pref_summary, filter_summary)
	user_prompt = build_user_prompt(req.query, retrieved_items)
	try:
		answer = generate_response(system_prompt, user_prompt)
	except GeminiConfigError as exc:
		raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
	except GeminiServiceError as exc:
		raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
	except Exception as exc:  # pragma: no cover
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)+" : Model generation failed.") from exc

	# Save conversation + messages
	conversation_id = req.conversation_id
	if not conversation_id:
		conv = models.Conversation(user_id=user.id, title=req.query[:100])
		db.add(conv)
		db.commit()
		db.refresh(conv)
		conversation_id = conv.id

	# If we still don't have a valid conversation_id, return an error instead of
	# trying to serialize an invalid ChatResponse.
	if conversation_id is None:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Conversation could not be created. Please try again.",
		)
	# messages
	user_msg = models.Message(conversation_id=conversation_id, role="user", content=req.query)
	def _to_citation(item: Dict[str, Any]) -> Dict[str, Any]:
		metadata = item.get("metadata") or {}
		doc_text = item.get("document") or ""

		# Prefer explicit rating fields from metadata; support both DB (stars) and API (rating).
		rating = metadata.get("rating")
		if rating is None:
			rating = metadata.get("stars")

		review_count = metadata.get("review_count") or metadata.get("user_ratings_total")

		# Heuristic: if this came from DB ingestion, the document may contain a
		# "Sample reviews:" section; try to pull one random sentence from it.
		random_review = None
		if "Sample reviews:" in doc_text:
			after = doc_text.split("Sample reviews:", 1)[1].strip()
			sentences = [s.strip() for s in after.split(".") if s.strip()]
			if sentences:
				random_review = random.choice(sentences)
				if not random_review.endswith("."):
					random_review += "."
		elif doc_text:
			# Fallback: short snippet from the document as a pseudo‑review.
			random_review = (doc_text[:220] + "...") if len(doc_text) > 220 else doc_text

		return {
			"id": item.get("id"),
			"title": metadata.get("title") or metadata.get("name"),
			"url": metadata.get("url"),
			"rating": rating,
			"review_count": review_count,
			"random_review": random_review,
		}

	assistant_msg = models.Message(
		conversation_id=conversation_id,
		role="assistant",
		content=answer,
		citations=[_to_citation(it) for it in retrieved_items],
	)
	db.add(user_msg)
	db.add(assistant_msg)
	db.commit()

	citations = assistant_msg.citations or []
	return ChatResponse(answer=answer, citations=citations, conversation_id=conversation_id)



