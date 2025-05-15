from app.services.search import google, alpha_vantage

# result = google.google_search("machine learning")


news_sentiment = alpha_vantage.fetch_news_sentiment

ticker = 'AAPL' 

global_news = news_sentiment()

# stock_news = news_sentiment(ticker)


print(global_news) 