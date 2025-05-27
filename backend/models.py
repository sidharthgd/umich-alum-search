
import sqlite3

def connect_db():
    return sqlite3.connect("db.sqlite3")

def search_alumni(query):
    con = connect_db()
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
    return [dict(zip(["name", "major", "current_company", "current_position", "previous_companies", "linkedin"], row)) for row in rows]
