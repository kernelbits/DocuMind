from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os 


load_dotenv()
QDRANT_URL= os.getenv('QDRANT_URL')
QDRANT_API = os.getenv('QDRANT_API_KEY')

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API
)

print(qdrant_client.get_collections())