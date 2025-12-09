from processor import PDFProcessor
from database import collection
import re

MAX_CONTEXT_CHARS = 2000

def _normalize_chunk_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def retrieve_context(user_query: str) -> str:
    processor = PDFProcessor()
    try:
        query_emb = processor.embed_query(user_query)
    except Exception:
        return ""

    if isinstance(query_emb, (list, tuple)) and query_emb and not isinstance(query_emb[0], (list, tuple)):
        query_emb = [query_emb]

    try:
        res = collection.query(query_embeddings=query_emb, n_results=5)
    except Exception:
        return ""

    documents = res.get("documents") or []
    if not documents or not documents[0]:
        return ""

    raw_chunks = documents[0]

    seen = set()
    unique_chunks = []
    for c in raw_chunks:
        if not isinstance(c, str):
            c = str(c)
        normalized = _normalize_chunk_text(c)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_chunks.append(normalized)

    if not unique_chunks:
        return ""

    formatted_blocks = []
    total_chars = 0
    for idx, chunk in enumerate(unique_chunks):
        block = f"[Source {idx+1}]\n{chunk}\n"
        if total_chars + len(block) > MAX_CONTEXT_CHARS:
            break
        formatted_blocks.append(block)
        total_chars += len(block)

    context = "\n---\n".join(formatted_blocks)
    return context