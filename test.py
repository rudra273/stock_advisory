from app.services.search import google, alpha_vantage, finnhub, news_org

ticker = 'AAPL' 
indian = "RELIANCE power"

# Google 
# result = google.google_search("machine learning")


# Alpha vantage 
# news_sentiment = alpha_vantage.fetch_news_sentiment
# global_news = news_sentiment()
# stock_news = news_sentiment(ticker)


# Finnhub 
# general_news = finnhub.fetch_general_news()
# company = finnhub.fetch_company_news(ticker)  # INdian company not workking 


# NEWS ORG
# news = news_org.fetch_news()
# indian = news_org.fetch_indian_news(stock="RELIANCE power")

print(indian) 