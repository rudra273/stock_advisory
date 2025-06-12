# app/services/search/news_org.py

import requests
from app.core.config import settings

api_key = settings.NEWSAPI_KEY

def fetch_news(query="Indian stock market", sort="publishedAt", limit=10):
    """
    Fetches news articles using NewsAPI's /v2/everything endpoint.

    Parameters:
        query (str): Search query (e.g., 'Indian stock market').
        sort (str, optional): Sort order ('publishedAt', 'relevancy', 'popularity'). Defaults to 'publishedAt'.
        limit (int, optional): Maximum number of articles (1 to 100). Defaults to 10.

    Returns:
        list: A list of dictionaries containing news article details.
    """
    if not api_key:
        raise ValueError("API key not found. Please set 'NEWSAPI_KEY' in your .env file.")

    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": sort,
        "pageSize": limit, 
        "apiKey": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok" and "articles" in data:
            news_items = []
            for article in data["articles"][:limit]:
                news = {
                    "source_name": article.get("source", {}).get("name", "N/A"),
                    "title": article.get("title", "N/A"),
                    "description": article.get("description", "N/A"),
                    "url": article.get("url", "N/A"),
                    "published_at": article.get("publishedAt", "N/A"),
                    "content": article.get("content", "N/A")
                }
                news_items.append(news)
            return news_items
        else:
            print("No news data found.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []




def fetch_indian_news(query=None, stock='company', sort="publishedAt", limit=10):
    """
    Fetches news articles related to the Indian stock market from specific domains using NewsAPI.

    Parameters:
        query (str): Search query (e.g., 'Indian stock market').
        stock (str, optional): Specific stock name or ticker to include in the search.
        sort (str, optional): Sort order ('publishedAt', 'relevancy', 'popularity'). Defaults to 'publishedAt'.
        limit (int, optional): Maximum number of articles (1 to 100). Defaults to 10.

    Returns:
        list: A list of dictionaries containing news article details.
    """
    if not api_key:
        raise ValueError("API key not found. Please set 'NEWSAPI_KEY' in your .env file.")

    base_url = "https://newsapi.org/v2/everything"
    domains = ",".join([
        "moneycontrol.com",
        "economictimes.indiatimes.com",
        "livemint.com",
        "business-standard.com",
        "financialexpress.com",
        "cnbctv18.com"
    ])

    # Construct the query string
    if stock:
        search_query = f"{query} {stock}"
    else:
        search_query = query

    # print('search query in news api -----------------', search_query)

    params = {
        "q": search_query,
        "language": "en",
        "sortBy": sort,
        "pageSize": limit,
        "domains": domains,
        "apiKey": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok" and "articles" in data:
            news_items = []
            for article in data["articles"][:limit]:
                news = {
                    "source_name": article.get("source", {}).get("name", "N/A"),
                    "title": article.get("title", "N/A"),
                    "description": article.get("description", "N/A"),
                    "url": article.get("url", "N/A"),
                    "published_at": article.get("publishedAt", "N/A"),
                    "content": article.get("content", "N/A")
                }
                news_items.append(news)
            return news_items
        else:
            print("No news data found.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
