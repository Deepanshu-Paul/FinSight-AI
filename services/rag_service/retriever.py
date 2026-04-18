import os
from sentence_transformers import SentenceTransformer
import faiss

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "/app/data/knowledge/faiss_index.bin"
DOC_PATH = "/app/data/knowledge/fraud_rules.txt"

# -----------------------------
# Load documents safely
# -----------------------------
docs = []

if os.path.exists(DOC_PATH):
    with open(DOC_PATH, "r") as f:
        docs = f.readlines()
else:
    print("⚠️ Warning: fraud_rules.txt not found. Using fallback knowledge.")
    docs = [
        "No knowledge base available.",
        "Fraud detection typically involves anomaly detection and pattern analysis."
    ]

# -----------------------------
# Load FAISS index safely
# -----------------------------
index = None

if os.path.exists(INDEX_PATH):
    try:
        index = faiss.read_index(INDEX_PATH)
        print("✅ FAISS index loaded successfully")
    except Exception as e:
        print(f"⚠️ Error loading FAISS index: {e}")
        index = None
else:
    print("⚠️ FAISS index not found. Retrieval will fallback to basic docs.")

# -----------------------------
# Retrieval function
# -----------------------------
def retrieve(query, k=2):
    """
    Retrieve top-k relevant documents based on query.
    Falls back gracefully if index is unavailable.
    """

    # If no index, return fallback docs
    if index is None:
        return docs[:k]

    try:
        query_vec = model.encode([query])
        distances, indices = index.search(query_vec, k)

        results = []
        for i in indices[0]:
            if i < len(docs):
                results.append(docs[i])

        return results

    except Exception as e:
        print(f"⚠️ Retrieval error: {e}")
        return docs[:k]