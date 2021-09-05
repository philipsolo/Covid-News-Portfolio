import ast
from flask_dir.database_store import fetch_article_recent, fetch_article_org
import random


def grab_all_recent(limit, top_results=10):
    articles = fetch_article_recent('newsdb', limit)
    random.shuffle(articles)
    key_words = {}
    temp_art = {}
    news_providers = {}
    for art in articles:
        news_providers[art['name']] = art['image']
        temp_art[art['articleLink']] = art
        text_dict = ast.literal_eval(art['sentiment'])
        for word in text_dict['common'].keys():
            if word not in key_words:
                key_words[word] = {'count': 1, 'word': word, 'urls': [art['articleLink']]}
            else:
                key_words[word]['count'] += 1
                key_words[word]['urls'].append(art['articleLink'])
    top_10 = sorted(key_words.values(), key=lambda k: k['count'])[-top_results:]
    print(news_providers)
    return {'metadata': {'art_len': len(temp_art), 'sources': news_providers}, 'articles': temp_art,
            'top_words': top_10}


def organize_text(articles):
    print(articles)


# For Specific Articles
def article_by_org(page_number, limit):
    offset = (limit * page_number) - limit

    articles = fetch_article('newsdb', limit, offset)

    print(fetch_article_brand('newsdb', 'name', 'CNN'))


if __name__ == '__main__':
    print("Running from within")
    print(grab_articles(1, 6))
