import os
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "/app/data/knowledge/faiss_index.bin"

docs = []
with open("/app/data/knowledge/fraud_rules.txt", "r") as f:
    docs = f.readlines()

# ✅ Safe load
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = None


def retrieve(query, k=2):
    if index is None:
        return ["No knowledge base available yet."]

    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, k)
    return [docs[i] for i in indices[0]]