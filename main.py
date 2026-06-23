import sqlite3

conn = sqlite3.connect("museum.db")
cursor = conn.cursor()

# create user table 
try:
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        pin INTEGER NOT NULL
    )
    """)
    print("Database created!")
except sqlite3.Error as e:
    print("User table creation error!")


def register():
    username = input("Enter your username (): ")
    pin = input("Enter your PIN (4 digits): ")
    
    if len(username) <= 4:
        print("Username is too short (5 characters minimum)")
        return

    if not pin.isdigit():
        print("PIN must contain only numbers")
        return

    if len(pin) != 4:
        print("PIN must be exactly 4 digits")
        return

    pin = int(pin)
    conn = sqlite3.connect("museum.db")
    cursor = conn.cursor()

    try: 
        cursor.execute("""
        INSERT INTO users (username, pin)
        VALUES (?, ?)
        """
        )
        conn.commit()
    except sqlite3.Error as e::
        print("User creation error!")


conn.commit()
conn.close()