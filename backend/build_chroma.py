
import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb import PersistentClient

# Load alumni JSON
with open("../data/alum-data.json", "r") as f:
    alumni_data = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents, metadatas, ids = [], [], []

for i, alum in enumerate(alumni_data):
    desc = (
        f"{alum['name']} is a {alum['current_position']} at {alum['current_company']}. "
        f"They majored in {alum['major']}. "
        f"Previously worked at {', '.join(alum['previous_companies'])}."
    )
    documents.append(desc)
    metadatas.append({
        "name": alum["name"],
        "major": alum["major"],
        "current_company": alum["current_company"],
        "current_position": alum["current_position"],
        "previous_companies": ", ".join(alum["previous_companies"]),
        "linkedin": alum["linkedin"]
    })
    ids.append(f"alum-{i}")

embeddings = model.encode(documents).tolist()

client = PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="alumni")
collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)

print("✅ ChromaDB built and persisted to ./chroma_db")
