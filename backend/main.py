import os
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import models
from backend.database.db import Base, engine, get_db
from backend.services.gemini_service import (
	GeminiConfigError,
	GeminiServiceError,
	build_system_prompt,
	build_user_prompt,
	generate_response,
	get_embedding,
)
from backend.services.memory_service import (
	get_or_create_user,
	get_user_preferences,
	set_user_preferences,
	summarize_preferences,
)

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

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


def get_chroma_client() -> chromadb.PersistentClient:
	client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR, settings=Settings(allow_reset=False))
	return client


def get_or_create_collection(client: chromadb.PersistentClient, name: str = "places"):
	try:
		return client.get_collection(name)
	except Exception:
		return client.create_collection(name, metadata={"hnsw:space": "cosine"})


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


class ChatRequest(BaseModel):
	user_id: str
	query: str
	location_hint: Optional[str] = None
	update_preferences: Optional[Dict[str, str]] = None
	conversation_id: Optional[int] = None


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


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
	if not req.query or not req.query.strip():
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query text is required.")

	# Ensure user record and update preferences if provided
	user = get_or_create_user(db, external_user_id=req.user_id)
	if req.update_preferences:
		set_user_preferences(db, user.id, req.update_preferences)
	prefs = get_user_preferences(db, user.id)
	pref_summary = summarize_preferences(prefs)

	# Retrieve from Chroma
	client = get_chroma_client()
	col = get_or_create_collection(client)
	try:
		query_embedding = get_embedding(req.query + (" " + req.location_hint if req.location_hint else ""))
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

	retrieved_items: List[Dict[str, Any]] = []
	if results and results.get("ids"):
		for i in range(len(results["ids"][0])):
			item = {
				"id": results["ids"][0][i],
				"document": results["documents"][0][i],
				"metadata": results["metadatas"][0][i],
			}
			retrieved_items.append(item)

	# Build prompt and call Gemini
	system_prompt = build_system_prompt(pref_summary)
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
	# messages
	user_msg = models.Message(conversation_id=conversation_id, role="user", content=req.query)
	assistant_msg = models.Message(
		conversation_id=conversation_id,
		role="assistant",
		content=answer,
		citations=[{
			"id": it["id"],
			"title": it.get("metadata", {}).get("title"),
			"url": it.get("metadata", {}).get("url"),
		} for it in retrieved_items]
	)
	db.add(user_msg)
	db.add(assistant_msg)
	db.commit()

	citations = assistant_msg.citations or []
	return ChatResponse(answer=answer, citations=citations, conversation_id=conversation_id)



