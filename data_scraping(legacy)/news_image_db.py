import time
import feedparser
import requests
from google.cloud import storage
from flask_dir.database_store import fetch_brand, add_article

rss_feed = {}


def get_image(image_link):
    added = False
    response = requests.get(image_link)
    with open('../Nasa.png', "wb") as file:
        file.write(response.content)
        file.close()
        added = True
        print("Image Added")
    return added


def upload_blob(link):
    bucket_name = "flask-stuff"
    destination_blob_name = "Nasa.png"
    storage_client = storage.Client.from_service_account_json('key.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    try:
        blob.delete()
    except:
        print("Not inside")

    get_image(link)
    blob.upload_from_filename('Nasa.png')
    print("added to bucket")


def grab_with_images():
    links = [['Nasa', "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss"]]
    for index, value in enumerate(links):
        all_articles = fetch_brand('newsdb', 'name', value[0])
        nasa = feedparser.parse(value[1])
        if len(nasa.entries) > 0:
            try:
                old_image = all_articles[0]['image']
            except IndexError:
                old_image = 'Empty'

            article = nasa.entries[0]
            title = article.title
            article_link = article['links'][0]['href']
            image_link = article['links'][1]['href']
            summary = article['summary']
            image = 'https://storage.googleapis.com/flask-stuff/' + value[0] + '.jpeg'

            if old_image == image_link:
                print("Already in")
                pass
            else:
                upload_blob(image_link)

                rss_feed.update(
                    {value[0]: {"name": value[0], 'link': value[1], 'image': image, 'title': title,
                                'articleLink': article_link,
                                'summary': summary, "Time_accessed": time.strftime('%Y-%m-%d %H:%M:%S'),
                                'Scrape': 'ERROR'}})

                print(rss_feed)


def search_and_add():
    grab_with_images()

    if len(rss_feed) > 0:
        for key, value in rss_feed.items():
            add_article('news_long', rss_feed[key])


if __name__ == "__main__":
    print('runin')
    search_and_add()
