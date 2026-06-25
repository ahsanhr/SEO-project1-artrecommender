import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from data_get_and_processing.museum_data_req import *
from PIL import Image
from io import BytesIO
import requests as r
from curl_cffi import requests

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

# if __name__ == '__main__':
    # img_strip = create_image_strip(img_urls)
    # top_five = get_color_palette(img_strip)
    # print(top_five)
    # display_palette(top_five)
