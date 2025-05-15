from app.services.search import google, alpha_vantage, finnhub, news_org

from app.services.crawler.market_index import fear_greed_index, mmi

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
# indian = news_org.fetch_indian_news() # can add stock parameter

# print(indian) 


cnn_data = fear_greed_index()
mmi_data = mmi()

if cnn_data:
    print("--- CNN Fear & Greed Index ---")
    print(f"Score: {cnn_data['score']}")
    print(f"Rating: {cnn_data['rating']}")
    print(f"Last Updated: {cnn_data['last_updated']}")
    print(f"Source: {cnn_data['source']}")
else:
    print("Failed to retrieve CNN Fear & Greed Index.")

if mmi_data:
    print("\n--- Market Mood Index ---")
    print(f"Score: {mmi_data['score']}")
    print(f"Rating: {mmi_data['rating']}")
    print(f"Last Updated: {mmi_data['last_updated']}")
    print(f"Source: {mmi_data['source']}")
else:
    print("\nFailed to retrieve Market Mood Index.")
