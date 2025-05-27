from flask import Flask, request, jsonify
from flask_cors import CORS
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
import json

client = OpenAI(api_key="")

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("alumni")

app = Flask(__name__)
CORS(app)

def extract_filters_from_query(query):
    prompt = f"""You are an API assistant. Extract structured filters from natural language queries about Michigan alumni.
Return a JSON object with optional keys: "major", "current_company", "previous_company".

If a value is not mentioned in the query, omit it.

Example:
Query: "Find CS alumni who now works at Google and used to work at Meta"
Response:
{{
  "major": "Computer Science",
  "current_company": "Google",
  "previous_company": "Meta"
}}

Query: "{query}"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"OpenAI extraction error: {e}")
        return {}

@app.route("/hybrid_search")
def hybrid_search():
    query = request.args.get("q", "")
    filters = extract_filters_from_query(query)
    print("LLM extracted filters:", filters)
    query_embedding = model.encode([query]).tolist()

    chroma_filters = {}
    prev_company = None

    if "major" in filters:
        chroma_filters["major"] = filters["major"]
    if "current_company" in filters:
        chroma_filters["current_company"] = filters["current_company"]
    if "previous_company" in filters:
        prev_company = filters["previous_company"].lower()

    try:
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=30,
            where=chroma_filters if chroma_filters else None
        )
        matches = results["metadatas"][0]

        # Manual match for previous_company
        if prev_company:
            matches = [
                m for m in matches
                if prev_company in m["previous_companies"].lower()
            ]

        return jsonify(matches[:10])  # top 10
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
