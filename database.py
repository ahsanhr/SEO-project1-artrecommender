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
            username TEXT UNIQUE NOT NULL,
            pin INTEGER NOT NULL
        )
        """)
        # artwork table
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS artwork (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            museum TEXT NOT NULL,
            country TEXT NOT NULL,
            date_created TEXT,
            medium_url TEXT,
            url TEXT
        )
        """)
        #saved_artworks table 
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS saved_artworks (
            user_id INTEGER,
            artwork_id INTEGER,
            PRIMARY KEY (user_id, artwork_id),

            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (artwork_id) REFERENCES artwork(id)
        )
        """)
    
        conn.commit()
        print("Database created!")
    except sqlite3.Error as e:
        print("User table creation error!")
    finally:
        conn.close()