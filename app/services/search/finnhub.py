import os
import requests
from datetime import datetime, timedelta
from app.core.config import settings

api_key = settings.FINNHUB_API_KEY


def fetch_general_news(category='general', limit=10):
    """
    Fetches general market news using Finnhub's General News API.

    Parameters:
        category (str): News category. Options include 'general', 'forex', 'crypto', 'merger'.
        limit (int): Number of articles to retrieve.

    Returns:
        list: A list of dictionaries containing news article details.
    """
    if not api_key:
        raise ValueError("API key not found. Please set 'FINNHUB_API_KEY' in your environment variables.")

    base_url = 'https://finnhub.io/api/v1/news'
    params = {
        'category': category,
        'token': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Limit the number of articles returned
        news_items = []
        for article in data[:limit]:
            news = {
                'headline': article.get('headline', 'N/A'),
                'summary': article.get('summary', 'N/A'),
                'source': article.get('source', 'N/A'),
                'url': article.get('url', 'N/A'),
                'datetime': article.get('datetime', 'N/A')
            }
            news_items.append(news)
        return news_items

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def fetch_company_news(symbol=None, from_date=None, to_date=None):
    """
    Fetches news articles for a given stock symbol using Finnhub's Company News API.

    Parameters:
        symbol (str, optional): The stock ticker symbol (e.g., 'RELIANCE.NS').
        from_date (str, optional): Start date in 'YYYY-MM-DD' format. Defaults to 7 days ago.
        to_date (str, optional): End date in 'YYYY-MM-DD' format. Defaults to today.

    Returns:
        list: A list of dictionaries containing news article details.
    """
    if not api_key:
        raise ValueError("API key not found. Please set 'FINNHUB_API_KEY' in your environment variables.")

    base_url = 'https://finnhub.io/api/v1/company-news'

    # Set default dates if not provided
    if not to_date:
        to_date = datetime.now().strftime('%Y-%m-%d')
    if not from_date:
        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    if not symbol:
        raise ValueError("Symbol is required to fetch company news.")

    params = {
        'symbol': symbol,
        'from': from_date,
        'to': to_date,
        'token': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        news_items = []
        for article in data:
            news = {
                'headline': article.get('headline', 'N/A'),
                'summary': article.get('summary', 'N/A'),
                'source': article.get('source', 'N/A'),
                'url': article.get('url', 'N/A'),
                'datetime': datetime.fromtimestamp(article.get('datetime')).strftime('%Y-%m-%d %H:%M:%S') if article.get('datetime') else 'N/A'
            }
            news_items.append(news)
        return news_items

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
