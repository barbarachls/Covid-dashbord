"""Module that requests covid data, and can schedule/delete updates"""
import json
import logging
import requests
from flask import request

ARTICLES = []
DELETED_ARTICLES = []

logging.basicConfig(filename='dashboard.log',level=logging.DEBUG,
                    format= '%(levelname)s: %(asctime)s %(module)s '
                            '%(message)s' )

with open('config.json') as config_file:
    data = json.load(config_file)
api_key = data['API_key']


def news_API_request(covid_terms: str = 'Covid COVID-19 coronavirus') -> dict:
    """Return a dictionary of all the articles  that contains the covid terms,
    that are in english. They are sorted by the publish date. For each
    articles the source, author, title, description, url, publish date and the
    content is returned.

    :rtype: object
    :param covid_terms: arg1
    :return: return dictionary of articles
    """
    complete_url = 'https://newsapi.org/v2/everything?q=' + covid_terms + \
                   '&language=en&sortBy=publishedAt&apiKey=' + api_key
    all_articles = requests.get(complete_url).json()
    return all_articles

news_API_request()

def update_news():
    """Return a list of 5 articles. If some articles have been deleted by the
    user before. they would not be put back in the article list.

    :return: list of articles
    """
    logging.info(' articles have been updated')
    global ARTICLES
    all_articles = news_API_request()
    count = 0
    ARTICLES = []
    for i in range(len(all_articles['articles'])):
        article = (all_articles['articles'][i])
        if article not in DELETED_ARTICLES:
            ARTICLES.append(article)
            count += 1
            if count > 4:
                break
        else:
            continue

def news_articles():
    """Run the update news function from the covid_news_handling module

    :return: None
    """
    update_news()
    return ARTICLES


def delete_news_articles():
    """Deleted the news article for the list when the user delete it from the
    interface. It is deleted by requesting the notif=, which would be the
    title of the article, and searching through the list of dictionaries
    which article it correspond to the remove them from the articles list.
    It also add the article to the deleted articles list so that the article
    never comes up again.

    :return: None
    """
    logging.info(' article has been deleted from the interface')
    global DELETED_ARTICLES, ARTICLES
    remove_articles = request.args.get('notif')
    if remove_articles:
        del_news = list(filter(lambda art: art['title'] == remove_articles,
                               ARTICLES))
        DELETED_ARTICLES = DELETED_ARTICLES + del_news
        ARTICLES.remove(del_news[0])

update_news()
