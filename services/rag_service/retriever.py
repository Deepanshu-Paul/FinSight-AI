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


def retrieve(query, k=3):
    try:
        query_words = query.lower().split()

        # Fetch candidates
        results = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=20
        )[0]

        scored = []
        for r in results:
            text = r.payload["text"].lower()

            # simple keyword score
            score = sum(word in text for word in query_words)

            scored.append((score, r.payload["text"]))

        # sort best first
        scored.sort(reverse=True)

        return [text for score, text in scored[:k]]

    except Exception as e:
        print("Retriever error:", e)
        return ["Fallback: No context available."]