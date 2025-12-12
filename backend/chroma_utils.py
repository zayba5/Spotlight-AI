import os

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv


load_dotenv()


CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
if not CHROMA_PERSIST_DIR:
	raise RuntimeError("CHROMA_PERSIST_DIR is not set. Configure it in your environment or .env file.")
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)


def get_chroma_client() -> chromadb.PersistentClient:
	"""
	Return a persistent Chroma client using the configured CHROMA_PERSIST_DIR.
	"""
	client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR, settings=Settings(allow_reset=False))
	return client


def get_or_create_collection(client: chromadb.PersistentClient, name: str = "places"):
	"""
	Get an existing Chroma collection or create it if it does not exist.
	"""
	try:
		return client.get_collection(name)
	except Exception:
		return client.create_collection(name, metadata={"hnsw:space": "cosine"})