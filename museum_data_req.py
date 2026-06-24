import requests
import sqlalchemy as db
import pandas as pd

country_name = input("enter a country: ")
chicago_url = f'https://api.artic.edu/api/v1/artworks?place_of_origin={country_name}'
met_url = f'https://collectionapi.metmuseum.org/public/collection/v1/search?geoLocation={country_name}&q=""'
cleve_url = f'https://openaccess-api.clevelandart.org/api/artworks/?q={country_name}'

works_dict = {}

chi_response = requests.get(chicago_url)
chi_works = chi_response.json()['data']
for w in chi_works:
    art_title = w['title']
    art_id = w['id']
    artist = w['artist_display']
    link = f'https://www.artic.edu/artworks/{art_id}/{art_title}'
    iiif_img_id = w['image_id']
    image_url = f'https://www.artic.edu/iiif/2/{iiif_img_id}/full/843,/0/default.jpg'
    works_dict[art_title] = [artist, link, image_url]
# ok this is how you get chicago links.

met_response = requests.get(met_url)
met_works = met_response.json()['objectIDs']
for i in range (1, 10):
    art_id = met_works[i]
    temp_link = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{art_id}'
    art_req = requests.get(temp_link)
    work_object = art_req.json()
    artist = work_object['artistDisplayName']
    if artist == "":
        artist = "unknown"
    art_title = work_object['title']
    link = f'https://www.metmuseum.org/art/collection/search/{art_id}'
    image_url = work_object['primaryImage']
    works_dict[art_title] = [artist, link, image_url]
# this is how to get the MET's links

cleve_response = requests.get(cleve_url)
cleve_works = cleve_response.json()['data']
for w in cleve_works:
    culture = w['culture']
    art_title = w['title']
    creator_data = w['creators']
    if creator_data == []:
        artist = "unknown"
    else:
        artist = creator_data[0]['description']
    if w['images'] == {}:
        continue
    image_url = w['images']['web']['url']
    if country_name in culture:
        link = w['url']
        works_dict[art_title] = [artist, link, image_url]
# these are all the cleveland links

worksDF = pd.DataFrame.from_dict(works_dict, orient='index', columns=["artist", "website_link", "image_url"])
print(worksDF)
