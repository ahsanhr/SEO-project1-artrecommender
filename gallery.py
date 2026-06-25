# Allow user to add and delete artworks to their central gallery
import sqlite3
from database import get_connection

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
            artwork["website_link"],
            artwork["image_link"]
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

def display_saved_artwork(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT artwork.title, artwork.artist, artwork.link
        FROM artwork
            JOIN saved_artworks
                ON artwork.id = saved_artworks.artwork_id
            WHERE saved_artworks.user_id = ?
        """, (user_id,))
    
        artworks = cursor.fetchall()

        if not artworks:
            print("You have no saved artworks!")
            return

        for i, art in enumerate(artworks, start=1):
            print(f"{i}. {art[0]}")
            print(f"   Artist: {art[1]}")
            print(f"   Website Link: {art[2]}")
            print(f"   Image Link: {art[3]}")

    except: 
        print("Error displaying saved artworks:", e)

    finally:
        conn.close()
