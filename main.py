import sqlite3

conn = sqlite3.connect("museum.db")
cursor = conn.cursor()

# create user table 
try:
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        username TEXT UNIQUE NOT NULL
        pin INTEGER NOT NULL
    )
    """)
    print("Database created!")
except sqlite3.Error as e:
    print("User table creation error!")



conn.commit()
conn.close()