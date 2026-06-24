import requests
import pandas as pd

def get_country():
    country_name = input("enter a country: ")
    return country_name

def create_urls(country_name):
    chicago_url = f'https://api.artic.edu/api/v1/artworks?place_of_origin={country_name}'
    met_url = f'https://collectionapi.metmuseum.org/public/collection/v1/search?geoLocation={country_name}&q=""'
    cleve_url = f'https://openaccess-api.clevelandart.org/api/artworks/?q={country_name}'
    urls = {
        'chi': chicago_url,
        'met': met_url,
        'cleve': cleve_url
    }
    return urls

def get_chicago_works(chicago_url):
    chi_works_dict = {}
    chi_response = requests.get(chicago_url)
    chi_works = chi_response.json()['data']
    for i in range(1, 5):
        w = chi_works[i]
        art_title = w['title']
        art_id = w['id']
        artist = w['artist_display']
        link = f'https://www.artic.edu/artworks/{art_id}/{art_title}'
        iiif_img_id = w['image_id']
        image_url = f'https://www.artic.edu/iiif/2/{iiif_img_id}/full/843,/0/default.jpg'
        chi_works_dict[art_title] = [artist, link, image_url]

    return chi_works_dict


def get_met_works(met_url):
    met_works_dict = {}
    met_response = requests.get(met_url)
    met_works = met_response.json()['objectIDs']
    for i in range (1, 5):
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
        met_works_dict[art_title] = [artist, link, image_url]
    
    return met_works_dict


def get_cleveland_works(cleve_url):
    cleve_works_dict = {}
    cleve_response = requests.get(cleve_url)
    cleve_works = cleve_response.json()['data']
    for i in range(1, 5):
        w = cleve_works[i]
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

    return cleve_works_dict

def create_works_dict(urls):
    works_dict = {}
    works_dict.update(get_chicago_works(urls['chi']))
    works_dict.update(get_met_works(urls['met']))
    works_dict.update(get_cleveland_works(urls['cleve']))
    worksDF = pd.DataFrame.from_dict(works_dict, orient='index', columns=["artist", "website_link", "image_url"])
    return worksDF

