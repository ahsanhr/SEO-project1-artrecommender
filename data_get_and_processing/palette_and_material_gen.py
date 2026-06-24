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
workflow breakdown:
1. user inputs art they want analyzed via CLI
2. SQL query pulls all the image_urls from the SELECT query generated, puts it into an array
3. parse through the array using the pillow module
4. the images will be turned into a local strip of images
5. pipe this output into imagga with a POST request
'''

'''
response template: response = requests.get(
    'https://api.imagga.com/v2/colors?image_url=https://imagga.com/static/images/colors/sample.jpg',
    auth=('<api-key>', '<api-secret>'),
)
'''

