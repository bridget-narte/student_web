import sqlite3

DB_NAME = "school.db"

def init_db():
    con = sqlite3.connect(DB_NAME)
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



def getall(tablename: str) -> list:
    """Fetch all records from a given table."""
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {tablename}")
    rows = cur.fetchall()
    con.close()
    return [dict(row) for row in rows]


def getrecord(tablename: str, **kwargs) -> list:
    """Fetch records based on given column filters."""
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    condition = " AND ".join([f"{k}=?" for k in kwargs.keys()])
    values = tuple(kwargs.values())

    cur.execute(f"SELECT * FROM {tablename} WHERE {condition}", values)
    rows = cur.fetchall()
    con.close()
    return [dict(row) for row in rows]


def addrecord(tablename: str, **kwargs) -> bool:
    """Insert record dynamically into any table."""
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()

        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?" for _ in kwargs])
        values = tuple(kwargs.values())

        cur.execute(f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})", values)
        con.commit()
        con.close()
        return True
    except Exception as e:
        print("Error adding record:", e)
        return False


def updaterecord(tablename: str, id: int, **kwargs) -> bool:
    """Update record by ID."""
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()

        updates = ", ".join([f"{k}=?" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (id,)

        cur.execute(f"UPDATE {tablename} SET {updates} WHERE id=?", values)
        con.commit()
        con.close()
        return True
    except Exception as e:
        print("Error updating record:", e)
        return False


def deleterecord(tablename: str, id: int) -> bool:
    """Delete record by ID."""
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(f"DELETE FROM {tablename} WHERE id=?", (id,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print("Error deleting record:", e)
        return False
