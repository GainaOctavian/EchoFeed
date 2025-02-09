import datetime
from typing import List

import requests
from echofeed.common import config_info, api_classes as api_cls


def search_google(query, num_results=10):
    """
    Caută pe Google după un query dat și returnează numărul de rezultate specificat.
    """
    response = requests.get(
        config_info.GOOGLE_SEARCH_URL,
        params={
            "key": config_info.GOOGLE_API_KEY,
            "cx": config_info.GOOGLE_ENGINE_ID,
            "q": query,
            "num": num_results
        }
    )
    print(response.status_code)
    results = response.json()
    return results


def parse_search_results(results, keywords):
    """
    Parsează rezultatele căutării Google și returnează o listă de articole.
    """
    articles = []
    for item in results.get('items', []):
        title = item.get('title', '')
        snippet = item.get('snippet', '')
        url = item.get('link', '')

        # Simulează extragerea datei articolului
        # Într-o implementare reală, va trebui să faci request la URL și să parsezi conținutul paginii pentru a găsi data
        date = datetime.datetime.now().date().isoformat()

        article = api_cls.Article(
            title=title,
            content=snippet,
            url=url,
            date=date,
            keywords=keywords,
        )
        articles.append(article)
    return articles


def create_articles_from_search(query: str, keywords: list, num_results: int = 10) -> List[api_cls.Article]:
    results = search_google(query, num_results)
    articles = parse_search_results(results, keywords)
    return articles
