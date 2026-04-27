from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("faiss_index.bin")

with open("texts.txt", "r") as f:
    texts = f.readlines()

def search(query, k=3):
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, k)

    results = [texts[i] for i in indices[0]]
    return results