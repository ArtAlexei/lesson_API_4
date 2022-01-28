import os
import urllib
from pathlib import Path
import datetime
import telegram
import requests
from dotenv import load_dotenv


def main():
    load_dotenv()
    Path("images").mkdir(parents=True, exist_ok=True)
    nasa_api_key = os.getenv("NASA_API_KEY")
    telegram_api_key = os.getenv("TELEGRAM_API_KEY")
    
    #fetch_spacex_last_launch()
    #fetch_nasa_photos(nasa_api_key)
    #fetch_nasa_epic_photos(nasa_api_key)

    bot = telegram.Bot(telegram_api_key)
    bot.send_message(chat_id='-1001733936497', text="I'm sorry Dave I'm afraid I can't do that.")
  

def fetch_nasa_epic_photos(nasa_api_key):
    params = {'api_key': nasa_api_key}
    url = 'https://api.nasa.gov/EPIC/api/natural'
    response = requests.get(url, params=params)
    response.raise_for_status()
    nasa_photos = response.json()
    for photo in nasa_photos:
        photo_date = datetime.datetime.fromisoformat(photo['date'])
        photo_name = photo['image']
        formatted_date = photo_date.strftime("%Y/%m/%d")
        url = f'https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/{photo_name}.png'
        download_image(url, photo_name, params)


def fetch_nasa_photos(nasa_api_key):
    params = {'api_key': nasa_api_key, 'count': 30}
    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=params)
    response.raise_for_status()
    nasa_media = response.json()
    for number, media in enumerate(nasa_media):
        if media['media_type'] == 'image':
            file_name = f'nasa{number}{get_img_extension(media["url"])}'
            download_image(media['url'], file_name)


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v3/launches"
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()[35]['links']['flickr_images']
    for number, image in enumerate(images):
        download_image(image, f'spacex{number}.jpg')
        print(number)


def get_img_extension(url):
    img_path = urllib.parse.urlsplit(url).path
    _, img_extension = os.path.splitext(img_path)
    return img_extension


def download_image(url, file_name, params={}):
    file_path = f'images/{file_name}'

    response = requests.get(url, params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    main()
