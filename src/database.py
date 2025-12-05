# Connecting to database and managing data
import chromadb
from chromadb.config import Settings



db_client = chromadb.PersistentClient(path="./chromadb")
collection = db_client.get_or_create_collection("pdf_docs")