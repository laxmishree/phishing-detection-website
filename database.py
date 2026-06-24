import sqlite3

conn = sqlite3.connect("feedback.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS scans(
    url TEXT,
    result TEXT,
    score INTEGER
)
""")

conn.commit()

conn.close()

print("Database Created Successfully!")