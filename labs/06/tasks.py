import json
import os
import re
from urllib.parse import urlencode

import requests

"""
TODO: paste tokens into utils
TODO: $ pip install requests oauth2
"""
from utils import create_client

# Twitter API documentation: https://developer.twitter.com/en/docs.html
API_URL = 'https://api.twitter.com/1.1/'

# CLIENT is an instance of Http (https://httplib2.readthedocs.io/en/latest/libhttplib2.html#http-objects)
CLIENT = create_client()


def send_tweet(status):
    """
    1 point.
    Send a tweet with the given `status`.
    Return the response from client.request call.

    Use the provided `CLIENT` variable. Don't forget to urlencode the
    URL parameters.

    Example:
        res = send_tweet('Hello!')
        assert int(res['status']) == 2OO
    """
    pass


def what_guido_says(since, until, keyword):
    """
    2 points.
    Return a list of tweets originating from the Twitter account 'gvanrossum'
    that were posted between `since` and `until` and contain `keyword`.
    Each entry in the list should be a tuple (tweet_text, is_retweet).
    tweet_text should be the text of the tweet
    is_retweet is a boolean stating whether the tweet is a retweet or not

    Use the provided `CLIENT` variable. Don't forget to urlencode the
    URL parameters.

    Example:
        what_guido_says('2018-10-20', '2019-10-25', 'Python')
        # [('Nice use of Python language tools and Jupyter notebooks. https://t.co/haBLh6x7K8',
            False), ('@AndreLeitaoDev @llanga I invite you to join us on the typing-sig to discuss
            this further. https://t.co/GAqeEawlnJ', False)]
    """
    pass


def scrape_images(url):
    """
    3 points.
    Download the web page from the given `url` and find all images on the page.
    Then download each image and write it to the filesystem under its filename.

    Example:
        Web page asd.cz: <html>....<img src="images/ahoj.jpg" />...</html>

        scrape_images('http://asd.cz')
        # creates file 'ahoj.jpg' with the image content ('images/' is ignored)

    Hint:
        Either download the web page and parse the images using regular expressions
        (https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285),
        or use the MechanicalSoup (https://mechanicalsoup.readthedocs.io/en/stable/tutorial.html)
        library to extract images from the page (recommended).
    """
    pass


def bonus_catzz():
    """
    1 point (bonus).
    Download the latest 10 tweets from the Twitter account CatMemes.
    Download all images contained in those tweets and combine them into
    one large image containing the latest cat memes. Write the collage image
    to the filesystem.

    Hint: use the pillow library to merge images together
    """
    pass
