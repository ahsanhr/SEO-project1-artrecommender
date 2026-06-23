import requests
import sqlalchemy as db
import pandas as pd

country_name = input("enter a country: ")
chicago_url = f'https://api.artic.edu/api/v1/artworks?place_of_origin={country_name}'
met_url = f'https://collectionapi.metmuseum.org/public/collection/v1/search?geoLocation={country_name}&q=""'
cleve_url = f'https://openaccess-api.clevelandart.org/api/artworks/?q={country_name}'


works_dict = {}
ind = 0

chi_response = requests.get(chicago_url)
chi_works = chi_response.json()['data']
for w in chi_works:
    art_title = w['title']
    art_id = w['id']
    artist = w['artist_display']
    link = f'https://www.artic.edu/artworks/{art_id}/{art_title}'
    works_dict[ind] = [artist, art_title, link]
    ind += 1
# ok this is how you get chicago links.

met_response = requests.get(met_url)
met_works = met_response.json()['objectIDs']
for i in range (1, 10):
    art_id = met_works[i]
    temp_link = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{art_id}'
    art_req = requests.get(temp_link)
    work_object = art_req.json()
    artist = work_object['artistDisplayName']
    art_title = work_object['title']
    link = f'https://www.metmuseum.org/art/collection/search/{art_id}'
    works_dict[ind] = [artist, art_title, link]
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
    if "France" in culture:
        link = w['url']
        works_dict[ind] = [artist, art_title, link]
    ind += 1
# these are all the cleveland links

worksDF = pd.DataFrame.from_dict(works_dict, orient='index', columns=["artist", "title", "artwork_link"])
print(worksDF)


# below is a reference i made from a previous project:
# engine = db.create_engine('sqlite:///artworks.db')
# response = requests.get(url)
# print(response.status_code)
# artworks_request = response.json()


# works = artworks_request['data']
# works_dict = {}

# ind = 0
# for w in works:
#   works_dict[ind] = [w['id'], w['title']]
#   ind+=1


# worksDF = pd.DataFrame.from_dict(works_dict, orient='index', columns=["museum_id", "artwork_title"])
# worksDF.to_sql('artwork', con=engine, if_exists='replace', index=False)

# with engine.connect() as connection:
#    query_result = connection.execute(db.text("SELECT * FROM artwork;")).fetchall()
#    print(pd.DataFrame(query_result))
# '''
# current output:
# 200
#     museum_id                        artwork_title
# 0         277                 Kantharos (Wine Cup)
# 1         255                           Fish Plate
# 2         183                 Kantharos (Wine Cup)
# 3         164          Column-Krater (Mixing Bowl)
# 4       60561                               Bureau
# 5      116399                          Boy's Armor
# 6       99766         Untitled (Butterfly Habitat)
# 7       69454                             Bedcover
# 8       76776  Kyoto Evergreen (Furnishing Fabric)
# 9       71562                             Sunlight
# 10      30659                           Breakwater
# 11      18856                             Fountain

# YAYYY
# '''

# # art_id = w['id']
# # art_title = w['title']
# # art_url = https://www.artic.edu/artworks/{art_id}/{art_title}
