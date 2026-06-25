# Allow user to add and delete artworks to their central gallery
import sqlite3
from database import get_connection

# # results = []

#     results.append({
#         "title": art_title,
#         "artist": artist,
#         "link": link
#     })
    
#     choice = input("Enter artwork numbers (example: 1,3,5): ")
#     choices = [int(x.strip()) for x in choice.split(",")]

#     for numbers in choices:
#         artwork = results[number - 1]
#         save_artwork(user_id, artwork)

# ADD artwork to saved list
def save_artwork(user_id, artwork):
    conn = get_connection()
    cursor = conn.cursor()

    #check if artwork exist before saving
    cursor.execute(""" 
    SELECT id
        FROM artwork
        WHERE title = ? AND artist = ?
    """, (artwork["title"], artwork["artist"]))

    row = cursor.fetchone()

    #save artwork
    if row is None:
        cursor.execute(""" 
        INSERT INTO artwork(title, artist, link)
            VALUES (?, ?, ?)
        """, (
            artwork["title"],
            artwork["artist"],
            artwork["link"]
        ))
        artwork_id = cursor.lastrowid

    else:
        artwork_id = row[0]
    
    # add the artwork into the user saved artwork list

    cursor.execute("""
        INSERT OR IGNORE INTO saved_artworks(user_id, artwork_id)
        VALUES (?, ?)
    """, (user_id, artwork_id))

    conn.commit()
    conn.close()

    print(f"Saved: {artwork['title']}")


# # DELETE artwork from saved list
# def delete_artworks():

def display_saved_artwork():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor,execute("""
        SELECT artwork.link, artwork.link, artwork.link
            JOIN saved_artworks
                ON artwork.id = saved_artworks.artwork_id
            WHERE saved_artworks.user_id = ?
        """, (user_id,))
    
        artworks = cursor.fetchall()

        if not artworks:
            print("You have no saved artworks!")
            return

        for i, art in enumerate(artworks, start=1):
            print(f"{i}. {artwork[0]}")
            print(f"   Artist: {artwork[1]}")
            print(f"   Link: {artwork[2]}")
            print()

    except: 
        print("Error displaying saved artworks:", e)

    finally:
        conn.close()
