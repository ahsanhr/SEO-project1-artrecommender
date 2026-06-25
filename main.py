import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from database import create_tables
from auth import register, login, google_login
from gallery import *
from data_get_and_processing.museum_data_req import *
from data_get_and_processing.palette_and_material_gen import *

W = 60

def divider():
    print("\n" + "=" * W + "\n")

def section(title):
    print("\n" + "=" * W)
    print(f"\n  {title}\n")
    print("=" * W + "\n")

def browse(user):
    section("BROWSE — HOW IT WORKS")
    print("  1. Type a country name when prompted  (e.g. france, japan, italy)")
    print("  2. Artworks from that country will be listed with a number [0], [1] ...")
    print("  3. Choose '1. Save Artwork' from the menu, then type the artwork number")
    print("     to save it.  To save multiple at once, separate numbers with commas:")
    print("     e.g.  0, 2, 5")
    divider()
    input("  Press Enter to continue...")

    country_name = get_country()
    urls = create_urls(country_name)
    works_dict = create_works_dict(urls)
    display_dict = {}
    ind = 0
    for k, v in works_dict.items():
        display_dict[ind] = {
            "title": k,
            "artist": v['artist'],
            "website_link": v['website_link'],
            "image_link": v['image_link']
        }
        ind += 1

    section("BROWSE ARTWORKS")
    for k, v in display_dict.items():
        print(f"\n  [{k}] {v['title']}")
        print(f"      Artist  : {v['artist']}")
        print(f"      URL     : {v['website_link']}")
        divider()

    while True:
        section("BROWSE MENU")
        print("  1. Save Artwork   — type the number shown in [ ] next to the artwork")
        print("  2. Back")
        divider()
        choice = input("  Enter your choice (1 or 2): ").strip()

        if choice == "1":
            max_idx = len(display_dict) - 1
            raw = input(f"\n  Enter artwork number(s) to save [0–{max_idx}]"
                        f"\n  Tip: separate multiple numbers with commas  (e.g. 0, 2, 5): ").strip()
            nums = [n.strip() for n in raw.split(",")]
            valid = [n for n in nums if n.isdigit() and int(n) in display_dict]
            invalid = [n for n in nums if n not in valid]
            if invalid:
                print(f"\n  [!] Skipped invalid entries: {', '.join(invalid)}")
            if not valid:
                print(f"  [!] No valid numbers entered. Please enter numbers between 0 and {max_idx}.")
                continue
            for n in valid:
                save_artwork(user[0], display_dict[int(n)])
        elif choice == "2":
            return
        else:
            print("\n  [!] Please enter 1 or 2.")

def generate_color_palette(user_id):
    links = get_saved_image_links(user_id)
    img_strip = create_image_strip(links)
    top_five = get_color_palette(img_strip)
    display_palette(top_five)

def main():
    create_tables()
    user = None
    while True:
        if user is None:
            section("ART RECOMMENDER  —  MAIN MENU")
            print("  1. Register")
            print("  2. Login")
            print("  3. Login with Google")
            print("  4. Exit")
            divider()
            choice = input("  Enter your choice: ").strip()

            if choice == "1":
                register()
            elif choice == "2":
                user = login()
            elif choice == "3":
                user = google_login()
            elif choice == "4":
                break
            else:
                print("\n  [!] Not an option, try again.")

        if user is not None:
            section(f"MAIN MENU  —  Welcome, {user[1]}!")
            print("  1. Browse Artworks")
            print("  2. View Saved Artworks")
            print("  3. Logout")
            print("  4. Exit")
            divider()
            choice = input("  Enter your choice: ").strip()

            if choice == "1":
                browse(user)
            elif choice == "2":
                section("SAVED ARTWORKS")
                display_saved_artwork(user[0])
                divider()
                select = input("\n  Generate color palette from saved artworks? (Y/N): ").strip().upper()
                if select == 'Y':
                    generate_color_palette(user[0])
                elif select != 'N':
                    print("\n  [!] Not an option.")
            elif choice == "3":
                print(f"\n  Goodbye, {user[1]}!\n")
                user = None
            elif choice == "4":
                break
            else:
                print("\n  [!] Not an option, try again.")


if __name__ == '__main__':
    main()
