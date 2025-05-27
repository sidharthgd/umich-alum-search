
import sqlite3
import json

def init_db():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS alumni")
    cur.execute("""
        CREATE TABLE alumni (
            name TEXT,
            major TEXT,
            current_company TEXT,
            current_position TEXT,
            previous_companies TEXT,
            linkedin TEXT
        )
    """)
    con.commit()
    con.close()

def load_data(json_file="../data/alum-data.json"):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    with open(json_file, "r") as f:
        data = json.load(f)
        for alum in data:
            cur.execute("""
                INSERT INTO alumni (name, major, current_company, current_position, previous_companies, linkedin)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                alum.get("name", ""),
                alum.get("major", ""),
                alum.get("current_company", ""),
                alum.get("current_position", ""),
                ", ".join(alum.get("previous_companies", [])),
                alum.get("linkedin", "")
            ))
    con.commit()
    con.close()

if __name__ == "__main__":
    init_db()
    load_data()
