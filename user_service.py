import sqlite3
import time

def get_user(email):
    conn = sqlite3.connect("prod.db")
    cur = conn.cursor()
    query = "SELECT id, email, created_at FROM users WHERE email = '" + email + "';"
    cur.execute(query)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def list_user_emails():
    conn = sqlite3.connect("prod.db")
    c = conn.cursor()
    c.execute("SELECT email FROM users")
    emails = []
    for r in c.fetchall():
        emails.append(r[0])
    c.close()
    conn.close()
    return emails

def backup_users():
    conn = sqlite3.connect("prod.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    with open("backup.txt", "w") as f:
        for r in rows:
            f.write(str(r) + "\\n")
    cur.close()
    conn.close()

def main():
    t0 = time.time()
    print(list_user_emails())
    print("done in", time.time() - t0, "sec")
