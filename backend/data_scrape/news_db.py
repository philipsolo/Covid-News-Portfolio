import time
import feedparser
import json
from bs4 import BeautifulSoup
import re
from typing import Dict
from database_store import add_article, fetch_urls, update_brand, fetch_unescaped
import logging


def read_json():
    with open('rss.json') as f:
        data = json.load(f)
    return data


def get_image(entry, image_sub):
    soup = BeautifulSoup(str(entry), 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags if 'widght="1"' or 'height="1"' not in img]
    return next(iter(urls), image_sub)


def get_summary(entry):
    if hasattr(entry, 'summary'):
        cleaned = (re.sub("<.*?>", "", entry.summary))
        shortened = cleaned[:400] + (cleaned[400:] and '...')
    else:
        shortened = 'No Summary :('
    return shortened


def get_author(entry):
    if hasattr(entry, 'author'):
        author = entry.author
    else:
        author = 'Nobody'
    return author


def check_url(url_dict, new_url, source):
    if source in url_dict:
        print(new_url, url_dict[source])
        return False if new_url in url_dict[source] else True
    return True


def get_rss(data: Dict[str, dict]) -> int:
    """
    Queries RSS feeds from inserted Dict and adds to database
    :param data: RSS feed dict
    :return: amount of entries inserted to database
    """
    inserted = 0
    url_dict = fetch_urls()
    for item in data.items():
        feeder = feedparser.parse(item[1]['link'])
        for i in range(3):
            try:
                e = feeder.entries[i]
            except IndexError as error:
                log.warning(IndexError, error, 'Internet?')
                pass
            try:
                print("Adding", e.link)
                log.info("Adding")
                print(e.link, item[0])
                if check_url(url_dict, e.link, item[0]):

                    art_dict = {"name": item[0],
                                'url': item[1]['link'],
                                'image': get_image(e, item[1]['image']),
                                'title': e.title,
                                'articleLink': e.link,
                                'summary': get_summary(e),
                                'author': get_author(e),
                                "Time_accessed": time.strftime('%Y-%m-%d %H:%M:%S'),
                                "Scrape": item[1]['Scrape'],
                                }
                    resp = add_article('newsdb', art_dict)
                    if resp:
                        inserted += 1
                else:
                    log.info("Already in")
            except AttributeError as err:
                log.warning(AttributeError, err)
    return inserted


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    logging.basicConfig()
    rss = read_json()
    get_rss(rss)
