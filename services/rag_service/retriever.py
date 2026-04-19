import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

print("QDRANT URL loaded:", QDRANT_URL is not None)
print("QDRANT API key loaded:", QDRANT_API_KEY is not None)

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "fraud_rules"

# ✅ Load model ONCE
print("🚀 Loading embedding model (for queries)...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query, k=2):
    try:
        # ✅ Embed query locally
        query_vec = model.encode(query).tolist()

        # ✅ Search Qdrant
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vec,
            limit=k
        )

        return [r.payload["text"] for r in results]

    except Exception as e:
        print("Qdrant error:", e)
        return ["Fallback: No context available."]