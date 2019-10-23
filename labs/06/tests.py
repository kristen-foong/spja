import getpass
import hashlib
import os
import time

from tasks import scrape_images, send_tweet, what_guido_says, bonus_catzz


def test_send_tweet():
    res = send_tweet('{} says hi! (Timestamp: {})'
                     .format(getpass.getuser(), int(time.time())))
    assert int(res['status']) == 200


def test_what_guido_says():
    res = what_guido_says("2018-10-20", "2019-10-25", "Python")
    assert ('Nice use of Python language tools and Jupyter notebooks. https://t.co/haBLh6x7K8', False) in res
    assert ('@AndreLeitaoDev @llanga I invite you to join us on the typing-sig to discuss this further. https://t.co/GAqeEawlnJ', False) in res


def test_scrape_images():
    scrape_images('https://gvanrossum.github.io/')

    files = [
        ("IMG_2192.jpg", "3acd8b703ba49e8c55665a671b8f7fc1"),
        ("license_thumb.jpg", "4a102f542d23a831362d0e0366a4dd3d"),
        ("guido-headshot-2019.jpg", "63e59a20f5f56fbc652d95e76ce3956c")
    ]

    assert all([os.path.isfile(f) and md5(f) == hash for (f, hash) in files])


def test_bonus_catzz():
    bonus_catzz()


# https://stackoverflow.com/a/3431838/1107768
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
