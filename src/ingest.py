import os 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

DATA_PATH = "data/"
DB_PATH = "db/"

def create_vector_db():
    if not os.path.exists(DATA_PATH):
        print(f"Error : Folder {DATA_PATH} is not found")
        return 
    files = {f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")}
    if not files:
        print(f"No Pdf's found in {DATA_PATH}")
        return 
    
    print(f"Found {len(files)} PDF(s). Processing")

    documents = []

    for pdf_file in files:
        file_path = os.path.join(DATA_PATH,pdf_file)
        print(f"Loading : {pdf_file}")
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600,chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} text chunks")

    print("Loading Embedding model...")
    embedding_model = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("Saving to ChromaDB...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )
    print(f"Success Database saved to {DB_PATH}")

if __name__ == "__main__":
    create_vector_db()