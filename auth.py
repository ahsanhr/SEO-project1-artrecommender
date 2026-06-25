import sqlite3
from database import get_connection
import os 
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow


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

# load CLIENT_ID & CLIENT_SECRECT
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

print(CLIENT_ID)
print(CLIENT_SECRET)

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    },
    scopes=[
        "openid",
        "email",
        "profile",
    ],
)

# currently not working since redirect give us to laptop's localhost
credentials = flow.run_local_server(port=0)
# credentials = flow.run_console()
# cannot redirect to https://faxpanel-spherescholar-4000.codio.io/proxy/8080/

# credentials = flow.run_local_server(
#     host="0.0.0.0",
#     port=8080,
#     open_browser=False
# )

