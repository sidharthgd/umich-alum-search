
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def search_alumni(query):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    like = f"%{query}%"
    rows = cur.execute("""
        SELECT * FROM alumni
        WHERE LOWER(name) LIKE ?
        OR LOWER(major) LIKE ?
        OR LOWER(current_company) LIKE ?
        OR LOWER(current_position) LIKE ?
        OR LOWER(previous_companies) LIKE ?
    """, (like, like, like, like, like)).fetchall()
    con.close()
    return [dict(zip(
        ["name", "major", "current_company", "current_position", "previous_companies", "linkedin"], row
    )) for row in rows]

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = search_alumni(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
