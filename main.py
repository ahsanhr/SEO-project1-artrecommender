from database import create_tables
from auth import register, login

# menu/ flow for the app
def main():
    create_tables()
    user = None
    while True:
        # Log In page
        if user is None:
            print("""

                        ===== MAIN MENU =====
                        1. Register
                        2. Login
                        3. Exit 
            """ )
            choice = input("Enter your choice: ")

            if choice == "1":
                register()

            elif choice == "2":
                user = login()
            elif choice == "3":
                break
        # After authenticated, main interface
        if user is not None:
            print(f"""

                        ===== MAIN MENU (welcome {user[1]})  =====
                        1. Browse
                        2. View Saved Artworks
                        3. Exit 
            """ )
            choice = input("Enter your choice: ")

            if choice == "1":
                print("browsing, Ahsan is impplmenting this feature!")
                #browse()

            elif choice == "2":
                pass
            #     display_saved_artwork(user["id"])

            elif choice == "3":
                user = None
                continue
main()
