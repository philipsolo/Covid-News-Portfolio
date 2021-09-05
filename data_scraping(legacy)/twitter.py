#!/home/petersolo427/solomonidis-flask/myprojectenv/bin/python3
import time
import tweepy as tw
from flask_dir.database_store import insert_twitter
from data_scraping import config

trends = ['COVID19Gr', 'Χαρδαλιάς']
time_line = ['@kmitsotakis', '@NikosDendias', '@guyverhofstadt', '@vonderleyen', '@EU_Commission']
tweet_dict = {}


class Twit:
    def __init__(self):
        self.consumer_key = config['CONSUMER_KEY']
        self.consumer_secret = config['CONSUMER_SECRET']
        self.access_token = config['ACCESS_TOKEN']
        self.access_token_secret = config['ACCESS_TOKEN_SECRET']

        auth = tw.AppAuthHandler(self.consumer_key, self.consumer_secret)
        self.api = tw.API(auth)


def get_current_trend():
    search = god.api.trends_place(946738)
    print(search)
    name = search[0]['trends'][1]['name']
    trends.append(name)


def search_trends(keyword, total_tweets=3):
    print(keyword)
    search_result = tw.Cursor(god.api.search,
                              q=keyword,
                              lang='en').items(total_tweets)
    get_embedded(search_result)
    return search_result


def get_timeline(screen_name):
    limit = 1
    api = god.api
    status = tw.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended")
    for index, value in enumerate(status.items()):
        if index <= limit:
            get_embedded(str(value.id), True, screen_name)
            print(value.id)
        else:
            break


def get_embedded(search_result, status=False, name='empty'):
    if not status:
        for tweet in search_result:
            try:
                name = tweet.user.name
                tweet_id = tweet.id_str
                tweet_created = tweet.created_at

                oembed = god.api.get_oembed(tweet_id)
                link = f"https://twitter.com/user/status/" + tweet_id
                html = oembed['html'].strip()
                tweet_dict.update({tweet_id: {
                    'name': name, 'tweet_id': tweet_id, 'articleLink': link, 'html_content': html,
                    'tweet_created': tweet_created.strftime('%Y-%m-%d'), "Time_accessed": time.strftime('%Y-%m-%d '
                                                                                                        '%H:%M:%S')
                }})

            except IndexError as e:
                print(e)
                pass
    else:
        oembed = god.api.get_oembed(search_result)
        html = oembed['html'].strip()

        link = f"https://twitter.com/user/status/" + search_result

        tweet_dict.update({search_result: {
            'name': name, 'tweet_id': search_result, 'articleLink': link, 'html_content': html,
            'tweet_created': "From Id", "Time_accessed": time.strftime('%Y-%m-%d %H:%M:%S')
        }})


def search_and_add():
    for query in trends:
        search_trends(query)
    for query in time_line:
        get_timeline(query)

    print(tweet_dict)
    print(len(tweet_dict))
    # delete_table('twitter')
    for key in tweet_dict.keys():
        print('Adding', tweet_dict[key])
        insert_twitter(tweet_dict[key])


def search_by_id(tweet_id):
    api = god.api
    tweet_text = 'Empty'
    try:
        tweet = api.get_status(tweet_id)
        tweet_text = tweet.text
    except tw.error.TweepError:
        pass
    return tweet_text


if __name__ == '__main__':
    print("Running from within")
    god = Twit()

    search_and_add()
