def get_user_by_email(email):
    import sqlite3
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result
