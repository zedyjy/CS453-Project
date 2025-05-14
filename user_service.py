import sqlite3
from contextlib import closing
from typing import List, Tuple
import time
import os

DB_PATH = os.getenv("DB_PATH", "prod.db")

def get_user(email: str) -> Tuple[int, str, str] | None:
    """Fetch a single user row by e‑mail (id, email, created_at)."""
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            "SELECT id, email, created_at FROM users WHERE email = ?;",
            (email,)
        )
        return cur.fetchone()

def list_user_emails() -> List[str]:
    """Return all user e‑mails in a memory‑efficient way."""
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT email FROM users")
        return [row[0] for row in cur.fetchall()]

def backup_users(dest: str = "backup.txt") -> None:
    """Dump the entire users table to a plain‑text backup file."""
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

    with open(dest, "w", encoding="utf‑8") as fp:
        fp.writelines(f"{row!r}\\n" for row in rows)

def main() -> None:
    start = time.perf_counter()
    print(list_user_emails())
    print(f"done in {time.perf_counter() - start:.4f} s")
