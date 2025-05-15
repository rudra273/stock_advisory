import requests
from app.core.config import settings

api_key = settings.ALPHA_VANTAGE_API_KEY

def fetch_news_sentiment(ticker=None, sort='LATEST', limit=10):
    """
    Fetches news articles and sentiment scores using Alpha Vantage's News & Sentiment API.

    Parameters:
        ticker (str, optional): The stock ticker symbol (e.g., 'AAPL' or 'RELIANCE.NSE').
        sort (str, optional): Sort order of results ('LATEST' or 'RELEVANCE'). Defaults to 'LATEST'.
        limit (int, optional): Maximum number of articles to retrieve (1 to 100). Defaults to 10.

    Returns:
        list: A list of dictionaries containing news article details.
    """

    if not api_key:
        raise ValueError("API key not found. Please set 'ALPHA_VANTAGE_API_KEY' in your .env file.")

    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'NEWS_SENTIMENT',
        'apikey': api_key,
        'sort': sort,
        'limit': limit
    }

    if ticker:
        params['tickers'] = ticker

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'feed' in data:
            news_items = []
            for article in data['feed']:
                news = {
                    'title': article.get('title', 'N/A'),
                    'summary': article.get('summary', 'N/A'),
                    'source': article.get('source', 'N/A'),
                    'url': article.get('url', 'N/A'),
                    'time_published': article.get('time_published', 'N/A'),
                    'overall_sentiment_score': article.get('overall_sentiment_score', 'N/A'),
                    'overall_sentiment_label': article.get('overall_sentiment_label', 'N/A')
                }
                news_items.append(news)
            return news_items
        else:
            print("No news data found.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
