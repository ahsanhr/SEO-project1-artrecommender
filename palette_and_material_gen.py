import os
import requests
from dotenv import load_dotenv

load_dotenv()

imagga_key = os.getenv("IMAGGA_API_KEY")
imagga_secret = os.getenv("IMAGGA_API_SECRET")
imagga_auth = os.getenv("IMAGGA_AUTH_TOKEN")

if not imagga_key:
    raise ValueError("missing imagga API key")

color_gen_url = "https://api.imagga.com/v2/colors"

'''
response template: response = requests.get(
    'https://api.imagga.com/v2/colors?image_url=https://imagga.com/static/images/colors/sample.jpg',
    auth=('<api-key>', '<api-secret>'),
)
'''

