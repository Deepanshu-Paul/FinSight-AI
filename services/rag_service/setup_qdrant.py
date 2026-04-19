import os
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
print("HF key loaded:", HF_API_KEY is not None)
print("QDRANT URL loaded:", QDRANT_URL is not None)
print("QDRANT API key loaded:", QDRANT_API_KEY is not None)

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "fraud_rules"
from sentence_transformers import SentenceTransformer

print("🚀 Loading local embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text).tolist()


# Load docs
with open("data/knowledge/fraud_rules.txt", "r") as f:
    docs = f.readlines()


# Create collection
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# Upload data
points = []
for i, doc in enumerate(docs):
    vector = get_embedding(doc)

    points.append({
        "id": i,
        "vector": vector,
        "payload": {"text": doc}
    })

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("✅ Qdrant setup complete")