import re
import asyncio
import pyppeteer
import requests
from requests_html import AsyncHTMLSession
from database_store import update_brand, fetch_unescaped
import logging
from text_proc import analyze_text
from bs4 import BeautifulSoup


async def get_js(link):
    res = await asession.get(link)
    try:
        await res.html.arender()
    except pyppeteer.errors.TimeoutError as err:
        logging.warning(TimeoutError, err, link, "Could not Scrape JS")
    return {'scrape': res, 'link': link}


async def get_simple(link):
    try:
        res = await asession.get(link)
        return {'scrape': res, 'link': link}
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as error:
        logging.warning(error, "Could not Scrape Simple")


def clean_html(soup):
    """Remove html tags from a string"""
    html = str(soup.findAll('p', text=True)).strip()
    tags = re.compile('<.*?>')
    clean_2 = re.sub(tags, '', html)
    line_removed = clean_2.replace('\n', ' ').replace('\r', '').replace('’', ' ')
    return re.sub(r"[-()\"#”/@“—;:<>{}'`+=~|!?,]", "", line_removed).strip()


def scrape_art(async_session, article_list=None) -> int:
    """
    :param async_session: async/await session object 
    :param article_list: manual article list for debugging
    :return: int articles inserted
    """

    unescaped_dict = fetch_unescaped()
    tasks = []
    article_sum = 0

    # Use for with manual articles (debugging)
    if article_list:
        for url in lister:
            tasks.append(asyncio.ensure_future(get_js(url)))

    else:
        for key, value in unescaped_dict.items():
            if value['Scrape'] == 'JAVA':
                for url in value['urls']:
                    article_sum += 1
                    tasks.append(asyncio.ensure_future(get_js(url)))
            elif value['Scrape'] == 'ERROR':
                pass
            else:
                for url in value['urls']:
                    article_sum += 1
                    tasks.append(asyncio.ensure_future(get_simple(url)))

        logging.info("Articles to be scraped: ", article_sum)

    items_remaining = task_run(async_session, tasks, article_sum)
    return items_remaining


def task_run(async_session, tasks, items_remaining):
    done, _ = async_session.loop.run_until_complete(asyncio.wait(tasks))

    for res_func in done:
        if res_func.result():
            page = res_func.result()['scrape']
        else:
            continue
        if page:
            url = res_func.result()['link']
            soup = BeautifulSoup(str(page.text), 'html.parser')
            text = clean_html(soup)

            if len(text) > 0:
                word_analysis = analyze_text(text)

                logging.info("Adding DB: ", url, word_analysis)
                result = update_brand(
                    {
                        'link': url,
                        'article_text': text,
                        'stats': word_analysis
                    }
                )
                if result:
                    items_remaining -= 1
            logging.info("Remaining", items_remaining)
        else:
            logging.warning("Not Found", res_func)
    return items_remaining


if __name__ == "__main__":
    # Load Dict from string
    # color = pickle.loads(b64_color.decode('base64', 'strict'))
    lister = ['https://www.bbc.co.uk/news/technology-57399628']
    logging.basicConfig(filename='myapp.log')

    logging.info('Started')
    asession = AsyncHTMLSession()
    print(scrape_art(asession))
    logging.info('Finished')
