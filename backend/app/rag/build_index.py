from sentence_transformers import SentenceTransformer
import faiss
import sqlite3
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "database.db")

def load_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, quantity FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def build_index():
    data = load_products()

    texts = [
        f"Product: {name}, Category: {cat}, Quantity: {qty}"
        for name, cat, qty in data
    ]

    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)

    faiss.write_index(index, "faiss_index.bin")

    with open("texts.txt", "w") as f:
        for t in texts:
            f.write(t + "\n")

    print("FAISS index built!")

if __name__ == "__main__":
    build_index()