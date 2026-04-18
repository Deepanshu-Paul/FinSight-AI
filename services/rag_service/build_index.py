from sentence_transformers import SentenceTransformer
import faiss
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = []
with open("/app/data/knowledge/fraud_rules.txt", "r") as f:
    docs = f.readlines()

embeddings = model.encode(docs)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "/app/data/knowledge/faiss_index.bin")

print("Index built successfully")