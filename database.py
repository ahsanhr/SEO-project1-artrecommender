import sqlite3

def get_connection():
    return sqlite3.connect("museum.db")

# create user table/ artworks table / saved_artworks table
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # user table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            pin TEXT,
            google_id TEXT UNIQUE,
            email TEXT UNIQUE,
            name TEXT
        )
        """)
        #saved_artworks table 
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS saved_artworks (
            user_id INTEGER,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            website_link TEXT UNIQUE NOT NULL,
            image_link TEXT UNIQUE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        conn.commit()
        print("Database created!")
    except sqlite3.Error as e:
        print("User table creation error!")
    finally:
        conn.close()

