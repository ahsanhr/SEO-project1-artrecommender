# Allow user to add and view artworks to their central gallery
import sqlite3
from database import get_connection

def save_artwork(user_id, artwork):
    conn = get_connection()
    cursor = conn.cursor()

    #check if artwork exist before saving
    #save artwork
    cursor.execute("""
    INSERT INTO saved_artworks(user_id, title, artist, website_link, image_link)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        artwork["title"],
        artwork["artist"],
        artwork["website_link"],
        artwork["image_link"]
    ))
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
        SELECT title, artist, website_link
        FROM saved_artworks
        WHERE user_id = ?
        """, (user_id,))
        artworks = cursor.fetchall()
        
        if not artworks:
            print("You have no saved artworks!")
            return

        for i, art in enumerate(artworks, start=1):
            print(f"{i}. {art[0]}")
            print(f"   Artist: {art[1]}")
            print(f"   Website Link: {art[2]}")
            
        return artworks
    except Exception as e: 
        print("Error displaying saved artworks:", e)
    finally:
        conn.close()
