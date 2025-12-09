from processor import PDFProcessor
from database import collection
import re

# Maximum total characters of context to include in the prompt (tune for your model)
MAX_CONTEXT_CHARS = 2000

def _normalize_chunk_text(text: str) -> str:
    # Collapse whitespace and newlines into single spaces, trim
    return re.sub(r'\s+', ' ', text).strip()

def retrieve_context(user_query: str) -> str:
    """
    Retrieve top chunks for the query, dedupe, normalize, and return a
    context string composed of chunk blocks. Returns empty string on error/no results.
    """
    processor = PDFProcessor()
    try:
        query_emb = processor.embed_query(user_query)
    except Exception:
        return ""

    # Ensure shape is list-of-lists for a single query
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

    # Deduplicate while preserving order
    seen = set()
    unique_chunks = []
    for c in raw_chunks:
        if not isinstance(c, str):
            # ensure chunk is a string
            c = str(c)
        normalized = _normalize_chunk_text(c)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_chunks.append(normalized)

    if not unique_chunks:
        return ""

    # Build formatted context, stop when reaching MAX_CONTEXT_CHARS
    formatted_blocks = []
    total_chars = 0
    for idx, chunk in enumerate(unique_chunks):
        block = f"[Source {idx+1}]\n{chunk}\n"
        if total_chars + len(block) > MAX_CONTEXT_CHARS:
            # stop adding more chunks once we reach the budget
            break
        formatted_blocks.append(block)
        total_chars += len(block)

    # Join blocks with a clear separator
    context = "\n---\n".join(formatted_blocks)
    return context