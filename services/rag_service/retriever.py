import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "fraud_rules"


def retrieve(query, k=2):
    try:
        # ⚠️ No embedding here
        # Use simple keyword fallback for now
        results = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=k
        )[0]

        return [r.payload["text"] for r in results]

    except Exception as e:
        print("Qdrant error:", e)
        return ["Fallback: No context available."]