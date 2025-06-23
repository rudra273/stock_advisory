from sqlalchemy.orm import Session
from app.models.market_sentiment import MarketSentiment

def get_all_market_sentiments(db: Session):
    return db.query(MarketSentiment).all()


