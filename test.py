import sqlite3
from contextlib import closing

def get_user_by_email(email):
    with closing(sqlite3.connect("app.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()
