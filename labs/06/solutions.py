import json
import os
from io import BytesIO
from urllib.parse import urlencode

import mechanicalsoup
import requests
from PIL import Image
from utils import create_client

API_URL = 'https://api.twitter.com/1.1/'
CLIENT = create_client()


def send_tweet(status):
    query = {
        'status': status
    }
    url = "{}{}".format(API_URL, 'statuses/update.json?{}'.format(urlencode(query)))
    response, data = CLIENT.request(url, method='POST')
    return response


def what_guido_says(since, until, keyword):
    query = {
        "q": "{} since:{} until:{} from:gvanrossum".format(keyword, since, until)
    }
    search_url = "{}{}".format(API_URL, 'search/tweets.json?{}'.format(urlencode(query)))
    response, data = CLIENT.request(search_url)
    data = json.loads(data.decode('utf-8'))
    return [(s['text'], 'retweeted_status' in s) for s in data['statuses']]


def scrape_images(url):
    if url and url[-1] != "/":
        url = url + "/"

    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)
    page = browser.get_current_page()
    images = page.find_all("img")

    for image in images:
        if "src" in image.attrs:
            src = image.attrs["src"]
            img_url = src
            if "http" not in img_url:
                img_url = "{}{}".format(url, img_url)
            data = requests.get(img_url)
            with open(os.path.basename(src), "wb") as f:
                f.write(data.content)


def bonus_catzz():
    query = {
        "screen_name": "CatMemes",
        "count": "10"
    }
    url = "{}{}".format(API_URL, "statuses/user_timeline.json?{}"
                        .format(urlencode(query)))
    response, data = CLIENT.request(url)
    data = json.loads(data.decode('utf-8'))
    images = []

    for tweet in data:
        entities = tweet.get('entities')
        if entities:
            media = entities.get('media')
            if media:
                obj = media[0]
                media_url = obj.get('media_url')
                if media_url:
                    images.append(requests.get(media_url).content)

    # https://stackoverflow.com/a/30228308/1107768
    images = list(set(images))
    jpgs = [Image.open(BytesIO(image)) for image in images]

    rows = [[]]
    for jpg in jpgs:
        if len(rows[-1]) == 3:
            rows.append([])
        rows[-1].append(jpg)

    widths = [sum(im.width for im in r) for r in rows]
    heights = [max(im.height for im in r) for r in rows]

    collage = Image.new('RGB', (max(widths), sum(heights)))

    pos = (0, 0)
    for r, row in enumerate(rows):
        for image in row:
            collage.paste(image, pos)
            pos = (pos[0] + image.width, pos[1])
        pos = (0, pos[1] + heights[r])

    collage.save('cat-collage.jpg')
