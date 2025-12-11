# Spotlight AI

Spotlight AI is a RAG-powered local recommendations assistant. Users ask natural-language questions (e.g., “best quiet coffee shop near me”) and the service summarizes reviews, menus, and ratings, tailoring results to their preferences over time.

## Architecture

```
spotlight-ai/
├── backend/
│   ├── main.py                  # FastAPI app + endpoints
│   ├── services/                # Gemini + memory helpers
│   ├── database/                # SQLAlchemy models and session setup
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit UI
│   └── requirements.txt
└── README.md
```

- **FastAPI** orchestrates the RAG flow and persists chat history.
- **Google Gemini** (`google-genai`) provides text generation and embeddings.
- **ChromaDB** stores dense vectors for retrieval.
- **PostgreSQL** holds user, preference, conversation, and message history.

---

## Prerequisites
- Python 3.10+
- PostgreSQL 13+ (local or remote)
- A Google AI Studio API key with access to Gemini.
- Optional: pgAdmin for DB management and Postman for API testing.

---

## Backend Setup

1. **Create & activate a virtual environment**
   ```powershell
   cd Spotlight-AI
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**
   ```powershell
   pip install -r backend/requirements.txt
   ```

3. **Provision PostgreSQL**
   - Launch pgAdmin (or use `psql`).
   - Create database `db_name`.

4. **Configure environment variables**
   Create `.env` (copy from `.env.example` if provided):
   ```
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/db_name
   CHROMA_PERSIST_DIR=./chroma_persistent_directory_name
   GEMINI_API_KEY=your_google_ai_studio_key
   GEMINI_GENERATE_MODEL=gemini_model_name
   GEMINI_EMBED_MODEL=gemini_embed_model_name
   ```
   Notes:
   - `CHROMA_PERSIST_DIR` is the path where Chroma writes embeddings; the default directory (`chromadb/`) is ignored by Git.
   - You can also use `GOOGLE_API_KEY` instead of `GEMINI_API_KEY`.

5. **Start the backend**
   ```powershell
   uvicorn backend.main:app --reload
   ```
   - The app should log “Application startup complete”.
   - Check `http://localhost:8000/health` → `{"status":"ok"}`.

---

## Frontend Setup

1. Activate the venv (if not already) and install Streamlit dependencies:
   ```powershell
   pip install -r frontend/requirements.txt
   ```

2. Run Streamlit:
   ```powershell
   streamlit run frontend/app.py
   ```

3. The UI launches at `http://localhost:8501`. Use the sidebar to verify backend health, set preferences, and start chatting.