import bcrypt
from .database import get_connection

def register_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()

    # Hash password and store as bytes
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed, role)
    )
    conn.commit()
    conn.close()


def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT password, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if row:
        hashed_pw = row[0]
        # Ensure hashed_pw is bytes (SQLite returns BLOB as bytes in Python 3)
        if isinstance(hashed_pw, str):
            hashed_pw = hashed_pw.encode('utf-8')

        if bcrypt.checkpw(password.encode(), hashed_pw):
            return row[1]
    return None


def user_exists(username):
    """Check if user exists in DB"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists
