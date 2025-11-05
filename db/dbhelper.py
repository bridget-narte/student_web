import os
import sqlite3

if os.environ.get("RENDER") or os.environ.get("VERCEL"):
    DB_PATH = "/tmp/school.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")


def init_db():
    """Initialize the database and create tables if needed."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idno TEXT UNIQUE NOT NULL,
            lastname TEXT NOT NULL,
            firstname TEXT NOT NULL,
            course TEXT NOT NULL,
            level INTEGER NOT NULL,
            photo TEXT
        )
    """)

    con.commit()
    con.close()


def get_connection():
    """Return a connection to the database."""
    return sqlite3.connect(DB_PATH)


def getall(tablename: str) -> list:
    con = get_connection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {tablename}")
    rows = cur.fetchall()
    con.close()
    return [dict(row) for row in rows]


def getrecord(tablename: str, **kwargs) -> list:
    con = get_connection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    condition = " AND ".join([f"{k}=?" for k in kwargs.keys()])
    values = tuple(kwargs.values())

    cur.execute(f"SELECT * FROM {tablename} WHERE {condition}", values)
    rows = cur.fetchall()
    con.close()
    return [dict(row) for row in rows]


def addrecord(tablename: str, **kwargs) -> bool:
    try:
        con = get_connection()
        cur = con.cursor()

        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?" for _ in kwargs])
        values = tuple(kwargs.values())

        cur.execute(f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})", values)
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(" Error adding record:", e)
        return False


def updaterecord(tablename: str, id: int, **kwargs) -> bool:
    try:
        con = get_connection()
        cur = con.cursor()

        updates = ", ".join([f"{k}=?" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (id,)

        cur.execute(f"UPDATE {tablename} SET {updates} WHERE id=?", values)
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(" Error updating record:", e)
        return False


def deleterecord(tablename: str, id: int) -> bool:
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(f"DELETE FROM {tablename} WHERE id=?", (id,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(" Error deleting record:", e)
        return False
