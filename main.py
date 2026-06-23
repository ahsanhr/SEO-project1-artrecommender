from database import create_tables
from auth import register, login

# menu/ flow for the app
def main():
    create_tables()
    while True:
        print("""

                    ===== MAIN MENU =====
                    1. Register
                    2. Login
                    3. Exit 
        """ )
        choice = input("Enter your choice: ")

        if choice == "1":
            register()

        if choice == "2":
            login()
        if choice == "3":
            break

main()
