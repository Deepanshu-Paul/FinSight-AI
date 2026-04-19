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


def simple_score(query_words, text):
    score = 0
    for word in query_words:
        if word in text:
            score += 2  # strong match
        if word in text.split():
            score += 1  # exact word bonus
    return score


def retrieve(query, k=3):
    try:
        query_words = [w for w in query.lower().split() if len(w) > 2]

        results, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=50   # increased candidate pool
        )

        scored = []

        for r in results:
            text = r.payload.get("text", "")
            text_lower = text.lower()

            score = simple_score(query_words, text_lower)

            if score > 0:
                scored.append((score, text))

        # fallback if nothing matches
        if not scored:
            return ["No strong match found in knowledge base."]

        scored.sort(key=lambda x: x[0], reverse=True)

        return [text for _, text in scored[:k]]

    except Exception as e:
        print("Retriever error:", e)
        return ["Fallback: No context available."]