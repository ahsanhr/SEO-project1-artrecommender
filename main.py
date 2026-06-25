from database import create_tables
from auth import register, login
from gallery import *
from data_get_and_processing.museum_data_req import *
from data_get_and_processing.palette_and_material_gen import *

def browse():
    country_name = get_country()
    urls = create_urls(country_name)
    works_dict = create_works_dict(urls)
    display_dict = {}
    ind = 0
    for k, v in works_dict.items():
        temp = {
            "title": k,
            "artist": v['artist'],
            "website_link": v['website_link'],
            "image_link": v['image_link']
        }
        display_dict[ind] = temp
        ind += 1
    print("""Format:
        NUMBER 
        TITLE 
        ARTIST 
        WEBSITE URL""")
    for k, v in display_dict.items():
        print(k)
        print(v["title"])
        print(v["artist"])
        print(v["website_link"])

    while True: 
        print("""
                ===== MENU =====
                1. Save Artwork
                2. Exit
        """ )
        choice = input("Enter your choice: ")
        if choice == "1":
            num = (input("Which artwork would you like to select? (Enter the number of 1 artwork at a time): "))
            if len(num) > 1:
                print("Sorry, try again!")
                continue
            elif not num.isdigit():
                print("Sorry, try again!")
                continue
            else:
                print("saving artwork..")
                save_artwork(user["id"], display_dict[num])
                continue
            
        elif choice == "2":
            return
        else:
            print("not an option!")
            continue

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
            else:
                continue
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
                browse()
            elif choice == "2":
                display_saved_artwork(user["id"])
            elif choice == "3":
                user = None
                continue
            else:
                continue


if __name__ == '__main__':
    main()