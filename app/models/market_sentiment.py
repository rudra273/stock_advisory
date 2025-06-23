from sqlalchemy import Column, Integer, String, DateTime
from app.db.config import Base
import datetime


class MarketSentiment(Base):
    __tablename__ = "market_sentiment"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)  # e.g., "CNN Fear & Greed Index"
    score = Column(Integer, nullable=False)
    rating = Column(String, nullable=False)
    last_updated = Column(String, nullable=False)  # ISO8601 or human-readable
    created_at = Column(DateTime, default=datetime.datetime.utcnow)