import bcrypt
from .database import get_connection


def register_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed, role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT password, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row[0]):
        return row[1]
    return None
