from processor import PDFProcessor
from database import collection

def retrieve_context(user_query: str) -> str:
    processor = PDFProcessor()
    query_emb = processor.embed_query(user_query)

    res = collection.query(
        query_embeddings=query_emb,
        n_results=3,
    )
    formatted_context = ""
    for index,chunk in enumerate(res['documents'][0]):
        formatted_context += f"Chunk {index+1}: {chunk}\n"

    return formatted_context