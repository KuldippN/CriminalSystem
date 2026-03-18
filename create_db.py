import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")

password = generate_password_hash("admin123")

cursor.execute("""
INSERT OR IGNORE INTO users (username,password)
VALUES (?,?)
""", ("admin", password))

conn.commit()
conn.close()

print("Database ready")