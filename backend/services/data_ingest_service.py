from typing import List, Optional

from sqlalchemy.orm import Session, selectinload

from backend.chroma_utils import get_chroma_client, get_or_create_collection
from backend.database.data_models import Business
from backend.services.gemini_service import GeminiConfigError, GeminiServiceError, get_embedding


def ingest_businesses_from_db(
	db: Session,
	max_rows: Optional[int] = None,
	min_review_count: Optional[int] = None,
	city: Optional[str] = None,
	batch_size: int = 100,
) -> int:
	"""
	Load rows from the `data.businesses` and `data.reviews` tables and upsert them into the Chroma collection.

	- You can limit work with `max_rows`, `min_review_count`, and `city` filters.
	- Records are processed in batches to keep memory usage and Chroma upsert size bounded.
	"""
	client = get_chroma_client()
	col = get_or_create_collection(client)

	query = db.query(Business).options(selectinload(Business.reviews))

	if min_review_count is not None:
		query = query.filter(Business.review_count >= min_review_count)
	if city:
		query = query.filter(Business.city == city)
	if max_rows is not None:
		query = query.limit(max_rows)

	total_ingested = 0

	current_ids: List[str] = []
	current_docs: List[str] = []
	current_metas: List[dict] = []
	current_embs: List[List[float]] = []

	for b in query.yield_per(batch_size):
		current_ids.append(str(b.business_id))

		# Sample a few review texts to include in the document
		review_texts = [r.text for r in (b.reviews or []) if r.text]
		sample_reviews = " ".join(review_texts[:3])

		base_desc = (
			f"{b.name} located at {b.address or ''}, {b.city or ''}, {b.state or ''} {b.postal_code or ''}. "
			f"Category: {b.category or 'Uncategorized'}. "
			f"Rating: {b.stars if b.stars is not None else 'N/A'} based on {b.review_count or 0} reviews. "
		)
		if sample_reviews:
			text = base_desc + f"Sample reviews: {sample_reviews}"
		else:
			text = base_desc + "No review text available."

		current_docs.append(text)
		# Metadata keys mirror fields defined in `backend/database/data_models.py`
		current_metas.append(
			{
				"business_id": b.business_id,
				"name": b.name,
				"address": b.address,
				"city": b.city,
				"state": b.state,
				"postal_code": b.postal_code,
				"category": b.categories,
				"stars": b.stars,
				"review_count": b.review_count,
			}
		)
		try:
			current_embs.append(get_embedding(text))
		except (GeminiConfigError, GeminiServiceError):
			# Fail fast if embedding generation is misconfigured or unavailable
			raise

		# Flush batch to Chroma to keep memory and request size bounded
		if len(current_ids) >= batch_size:
			col.upsert(ids=current_ids, documents=current_docs, metadatas=current_metas, embeddings=current_embs)
			total_ingested += len(current_ids)
			current_ids, current_docs, current_metas, current_embs = [], [], [], []

	# Flush any remaining items
	if current_ids:
		col.upsert(ids=current_ids, documents=current_docs, metadatas=current_metas, embeddings=current_embs)
		total_ingested += len(current_ids)

	return total_ingested
