from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.market_sentiment import MarketSentimentSchema
from app.repositories.get_market_sentiment import get_all_market_sentiments
from app.db.config import get_db

router = APIRouter(
    prefix="/market-sentiment",
    tags=["Market Sentiment"]
)
@router.get("/index", response_model=List[MarketSentimentSchema])
def read_market_sentiments(db: Session = Depends(get_db)):
    return get_all_market_sentiments(db)