import sqlite3

def get_connection():
    return sqlite3.connect("museum.db")

# create user table 
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pin INTEGER NOT NULL
        )
        """)
        conn.commit()
        print("Database created!")
    except sqlite3.Error as e:
        print("User table creation error!")
    finally:
        conn.close()