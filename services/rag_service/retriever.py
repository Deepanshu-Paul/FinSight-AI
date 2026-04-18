import os
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "/app/data/knowledge/faiss_index.bin"
DOC_PATH = "/app/data/knowledge/fraud_rules.txt"

docs = []

# ✅ SAFE FILE LOADING
if os.path.exists(DOC_PATH):
    with open(DOC_PATH, "r") as f:
        docs = f.readlines()
else:
    print("⚠️ fraud_rules.txt not found, using fallback")
    docs = [
        "No knowledge base available.",
        "Fraud detection typically involves anomaly detection and pattern analysis."
    ]

# ✅ SAFE INDEX LOADING
if os.path.exists(INDEX_PATH):
    try:
        index = faiss.read_index(INDEX_PATH)
    except:
        index = None
else:
    index = None


def retrieve(query, k=2):
    if index is None:
        return docs[:k]

    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, k)

    return [docs[i] for i in indices[0] if i < len(docs)]