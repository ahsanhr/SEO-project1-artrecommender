import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from data_get_and_processing.museum_data_req import *
from PIL import Image
from io import BytesIO
import requests as r
from curl_cffi import requests
from curl_cffi.requests.exceptions import HTTPError, RequestException

load_dotenv()

imagga_key = os.getenv("IMAGGA_API_KEY")
imagga_secret = os.getenv("IMAGGA_API_SECRET")
imagga_auth = os.getenv("IMAGGA_AUTH_TOKEN")

if not imagga_key:
    raise ValueError("missing imagga API key")

color_gen_url = "https://api.imagga.com/v2/colors"


#this function is from the PIL Image documentation
def merge(im1: Image.Image, im2: Image.Image) -> Image.Image:
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGB", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im

def create_image_strip(img_urls):
    in_memory_images = [] 
    for url in img_urls:
        if url == "":
            continue
        try:
            response = requests.get(url, impersonate="chrome120")
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")
            height = 400
            aspect_ratio = img.width / img.height
            width = int(height * aspect_ratio)
            resized = img.resize((width, height))
            in_memory_images.append(resized)
        except Exception as err:
            print(f'{err}, couldnt do {url}')

    result = in_memory_images[0]
    for imgs in in_memory_images:
        result = merge(result, imgs)

    result.convert("RGB").save("imagestrip.jpg", "JPEG")
    return "imagestrip.jpg"


def get_color_palette(imgfilename):
    #and this is from the imagga docs:
    with open(imgfilename, "rb") as f:
        resp = r.post(
            color_gen_url,
            files={"image": f},
            auth=HTTPBasicAuth(imagga_key, imagga_secret)
        )
    data = resp.json()

    colors =  data['result']['colors']['image_colors']

    top_five = sorted(colors, key=lambda x : x['percent'], reverse=True)[:5]

    return top_five

def display_palette(top_five):
    top_5_dict = {}
    print("\nYour Selected Work's Palette")
    for c in top_five:
        name = c['closest_palette_color']
        hex_code = c['html_code']
        top_5_dict[name] = [hex_code]
        print(f'- {name} | {hex_code}')
    return top_5_dict

if __name__ == '__main__':
    # c = get_country()
    # urls = create_urls('France')
    # working_df = create_works_df(urls)
    # img_urls = working_df['image_url'].tolist()
    # img_strip = create_image_strip(img_urls)
    # top_five = get_color_palette(img_strip)
    # print(top_five)
    # display_palette(top_five)
    dummy_top_five = [{'b': 216, 'closest_palette_color': 'star light', 'closest_palette_color_html_code': '#e7e9e7', 'closest_palette_color_parent': 'white', 'closest_palette_distance': 3.66573762893677, 'g': 217, 'html_code': '#d9d9d8', 'percent': 36.2092094421387, 'r': 217},
     {'b': 104, 'closest_palette_color': 'charcoal gray', 'closest_palette_color_html_code': '#80817d', 'closest_palette_color_parent': 'grey', 'closest_palette_distance': 8.73495674133301, 'g': 108, 'html_code': '#726c68', 'percent': 21.5512313842773, 'r': 114},
    {'b': 149, 'closest_palette_color': 'cathedral', 'closest_palette_color_html_code': '#9f9c99', 'closest_palette_color_parent': 'grey', 'closest_palette_distance': 1.32948362827301, 'g': 153, 'html_code': '#9e9995', 'percent': 20.0464973449707, 'r': 158},
    {'b': 163, 'closest_palette_color': 'champagne', 'closest_palette_color_html_code': '#baaa91', 'closest_palette_color_parent': 'light brown', 'closest_palette_distance': 4.60208702087402, 'g': 184, 'html_code': '#cab8a3', 'percent': 12.5917587280273, 'r': 202},
    {'b': 64, 'closest_palette_color': 'graphite', 'closest_palette_color_html_code': '#3a3536', 'closest_palette_color_parent': 'black', 'closest_palette_distance': 5.2254319190979, 'g': 67, 'html_code': '#484340', 'percent': 9.60130500793457, 'r': 72}]
    display_palette(dummy_top_five)
