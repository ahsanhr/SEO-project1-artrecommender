from gallery import save_artwork, display_saved_artwork

mock_artworks = [
    {
        "title": "The Starry Night",
        "artist": "Vincent van Gogh",
        "link": "https://example.com/starry-night"
    },
    {
        "title": "Water Lilies",
        "artist": "Claude Monet",
        "link": "https://example.com/water-lilies"
    }
]

user_id = 1

save_artwork(user_id, mock_artworks[0])
save_artwork(user_id, mock_artworks[1])

display_saved_artwork(user_id)