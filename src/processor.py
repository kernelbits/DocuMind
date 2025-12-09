from reader import PDFReader, TextChunker, Embedder

class PDFProcessor:
    def __init__(self):
        self.reader = PDFReader()
        self.chunker = TextChunker()
        self.embedder = Embedder()

    def process_pdf(self, path: str):
        text = self.reader.read(path)
        chunks = self.chunker.chunk(text)
        embeddings = self.embedder.encode(chunks)
        embeddings = [e.tolist() for e in embeddings]
        return chunks, embeddings

    def embed_query(self, query: str):
        emb =  self.embedder.encode([query])
        return emb[0].tolist()