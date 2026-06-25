import sqlite3
from database import get_connection
import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
import requests


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

# enabling Google OAuth 2.0

load_dotenv()

os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def google_login():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        },
        scopes=SCOPES,
    )

    credentials = flow.run_local_server(port=0)

    response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"},
    )
    user_info = response.json()

    google_id = user_info.get("sub")
    email = user_info.get("email")
    name = user_info.get("name")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO users (google_id, email, name) VALUES (?, ?, ?)",
            (google_id, email, name),
        )
        conn.commit()
        cursor.execute(
            "SELECT id, name FROM users WHERE google_id = ?", (google_id,)
        )
        user = cursor.fetchone()
        print(f"Welcome, {user[1]}!")
        return user
    except sqlite3.Error as e:
        print(f"Login error: {e}")
        return None
    finally:
        conn.close()
