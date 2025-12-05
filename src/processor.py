from reader import PDFReader, TextChunker, Embedder

class PDFProcessor:
    def __init__(self):
        self.reader = PDFReader()
        self.chunker = TextChunker()
        self.embedder = Embedder()

    def process_pdf(self, path: str):
        """Read → Chunk → Embed."""
        text = self.reader.read(path)
        chunks = self.chunker.chunk(text)
        embeddings = self.embedder.encode(chunks)
        return chunks, embeddings

    def embed_query(self, query: str):
        return self.embedder.encode([query])
