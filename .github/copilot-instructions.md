### Copilot / AI Agent Instructions for Spotlight-AI

Purpose: Help AI coding agents become productive quickly in this repository by
documenting the architecture, developer workflows, environment expectations,
and concrete code patterns to follow when modifying or extending the project.

1) Big-picture architecture
- Backend: FastAPI app at `backend/main.py` exposes endpoints: `/health`,
  `/ingest`, `/ingest_google_places`, `/ingest_db`, `/chat`. The FastAPI app
  composes services from `backend/services/` and persists chat data in
  `backend/database/`.
- Services: `backend/services/gemini_service.py` (text generation, embeddings,
  routing planner), `google_places_service.py` (live Places API),
  `data_ingest_service.py` (Postgres -> Chroma ingestion), and
  `memory_service.py` (user preferences and conversation helpers).
- Vector store: Chroma managed by `backend/chroma_utils.py`; persistence path is
  `CHROMA_PERSIST_DIR` (set via environment).
- Database: SQLAlchemy models in `backend/database/` (`models.py`, `data_models.py`),
  connection and session in `backend/database/db.py` (expects `DATABASE_URL`).

2) Key integration points and patterns
- Embeddings: call `get_embedding(text)` from `backend/services/gemini_service.py`.
  Agents should reuse this helper when adding embeddings. Example: ingest code
  uses `get_embedding(text)` and upserts into Chroma.
- Prompt building: use `build_system_prompt(pref_summary)` and
  `build_user_prompt(query, retrieved_items)` in `gemini_service.py`. When
  modifying LLM behavior, update these two functions rather than calling the
  SDK directly from handlers.
- Chroma usage: create/get collection via `get_or_create_collection(client,
  name='places')` and use `col.upsert(...)` and `col.query(...)` as shown in
  `backend/main.py` and `backend/services/data_ingest_service.py`.
- Error handling: services raise specific exceptions (e.g. `GeminiConfigError`,
  `GeminiServiceError`, `PlacesConfigError`, `PlacesServiceError`). FastAPI
  handlers map these to appropriate HTTP errors; preserve this separation.

3) Environment & runtime commands (exact)
- Required env vars (see `README.md` and `.env`):
  - `DATABASE_URL` (SQLAlchemy DB URL)
  - `CHROMA_PERSIST_DIR` (local path for Chroma persistent client)
  - `GEMINI_API_KEY` / `GOOGLE_API_KEY` and optional `GEMINI_GENERATE_MODEL`,
    `GEMINI_EMBED_MODEL`
  - `GOOGLE_PLACES_API_KEY` (for Places ingestion and live queries)
- Start backend locally:
  - `uvicorn backend.main:app --reload`
- Start frontend (Streamlit):
  - `streamlit run frontend/Homepage.py`
- Tests: backend uses pytest. Run from project root:
  - `pytest backend/tests` (or `pytest` to run everything)

4) Conventions & code patterns to follow
- Use helpers in `backend/services/` for external API access; avoid sprinkling
  raw calls to the Gemini SDK or HTTP clients outside these modules.
- When adding new metadata to upserted documents, match keys used in
  `data_ingest_service.py` and `ingest_google_places` (e.g., `title`,
  `address`, `source`, `place_id`) so downstream prompt formatting works.
- For embedding generation and retries, reuse `get_embedding` which encapsulates
  SDK differences and error wrapping — don't duplicate its parsing logic.
- DB interactions should use `get_db()` dependency from `backend/database/db.py`
  to ensure proper session lifecycle in FastAPI endpoints.

5) Small examples (copy/paste friendly)
- Build user prompt (example produced by `build_user_prompt`):
  - `build_user_prompt(query, retrieved_items)` formats retrieved chunks with
    numbered citations like `[1] Title ...` and instructs the model to return
    top recommendations and citation references.
- Ingest flow (example):
  - Use `get_chroma_client()` -> `get_or_create_collection(client)` ->
    `col.upsert(ids=..., documents=..., metadatas=..., embeddings=...)`.

6) What to avoid / preserve
- Do not hard-code API keys or DB URLs in code; use environment variables.
- Preserve existing exception classes and HTTP mapping; they encode expected
  operational behavior and tests rely on them.

7) Where to look for tests and examples
- `backend/tests/` contains pytest tests demonstrating expected service
  behavior and error handling. Use tests as canonical examples when adding
  features.

Feedback: If any runtime commands, files, or conventions are incorrect or
missing, tell me which parts need clarification and I will update this
document accordingly.
