from processor import PDFProcessor
from database import collection

processor = PDFProcessor()

# Read + Chunk + Embed
chunks, embeddings = processor.process_pdf("./data/norse.pdf")
print(embeddings.shape)

# Store in ChromaDB
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# Query
query = "What does this document talk about?"
query_emb = processor.embed_query(query)

res = collection.query(
    query_embeddings=query_emb,
    n_results=3
)

print(res)
