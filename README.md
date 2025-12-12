# Spotlight AI

Spotlight AI is a RAG-powered local recommendations assistant. Users ask natural-language questions (e.g., “best quiet coffee shop near me”) and the service summarizes reviews, menus, and ratings, tailoring results to their preferences over time.

## Architecture

```
spotlight-ai/
├── backend/
│   ├── main.py                  # FastAPI app + endpoints
│   ├── services/                # Gemini + Chroma data access + memory helpers
│   ├── database/                # SQL data access
│   ├── chroma_utils.py          # ChromaDB client + collection helpers
│   ├── tests/                   # Pytest-based backend tests
│   └── requirements.txt
├── frontend/
│   ├── Homepage.py              # Streamlit UI entry
│   └── pages/                   # Additional UI pages
└── README.md
```

- **FastAPI** orchestrates the retrieval-augmented generation (RAG) flow and persists chat history.
- **Google Gemini** (`google-genai`) provides text generation, embeddings, and routing decisions between data sources.
- **ChromaDB** stores dense vectors for retrieval.
- **PostgreSQL** holds user accounts, preferences, conversations, and external business/review data.
- **Google Places API** is used both for live retrieval and optional ingestion into Chroma.

## Prerequisites

- Python 3.10+  
- PostgreSQL 13+
- Google AI Studio / Gemini API key
- Google Places API key
- Optional: pgAdmin for DB management and Postman/curl for API testing.

---

## Backend setup

### 1. Create & activate a virtual environment

```powershell
cd Spotlight-AI
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 3. Provision PostgreSQL

- Launch pgAdmin (or use `psql`).  
- Create a database, e.g. `spotlight_ai`.  
- Optionally create a separate schema `data` for external business/review tables if you plan to use the Postgres ingestion.

### 4. Configure environment variables

Create a `.env` file in the project root (this file is ignored by Git):

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/spotlight_ai
CHROMA_PERSIST_DIR=./chromadb

# Gemini / Google AI Studio
GEMINI_API_KEY=your_google_ai_studio_key
GEMINI_GENERATE_MODEL=gemini-2.5-pro
GEMINI_EMBED_MODEL=text-embedding-004

# Google Places
GOOGLE_PLACES_API_KEY=your_google_places_key
```

Notes:
- `CHROMA_PERSIST_DIR` is the path where Chroma writes embeddings; choose any local directory (it is safe to ignore in Git).
- You can also use a shared `GOOGLE_API_KEY` instead of providing both `GEMINI_API_KEY` and `GOOGLE_PLACES_API_KEY`.

### 5. Start the backend

```powershell
uvicorn backend.main:app --reload
```

- The app should log application startup without errors.  
- Check `http://localhost:8000/health` → `{"status":"ok"}`.  
- Open `http://localhost:8000/docs` for interactive API docs.

---

## Frontend setup (Streamlit)

1. Activate the venv (if not already) and install Streamlit dependencies:

   ```powershell
   pip install -r frontend/requirements.txt
   ```

2. Run Streamlit:

   ```powershell
   streamlit run frontend/Homepage.py
   ```

3. The UI launches at `http://localhost:8501`. Use it to:
   - Verify backend health.
   - Set user preferences.
   - Chat with the assistant using the combined Postgres + Chroma + Google Places data. 