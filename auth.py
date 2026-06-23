import sqlite3
from database import get_connection


# user create account
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

    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("""
        INSERT INTO users (username, pin)
        VALUES (?, ?)
        """, (username, pin)
        )
        conn.commit()
        print("Account created")
    except sqlite3.Error as e:
        print("User creation error!")
    finally:
        conn.close()


# user login
def login():
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

    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("""
        SELECT id, username 
        FROM users
        WHERE username = ? and pin = ?
        """, (username, pin)
        )
        
        user = cursor.fetchone()

        if user:
            print(f"Welcome {username}")
            return user

        else:
            print("Invalid username or PIN")
            return None

    except sqlite3.Error as e:
        print("User creation error!")
    finally:
        conn.close()



