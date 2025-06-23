from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarketSentimentSchema(BaseModel):
    id: int
    source: str
    score: int
    rating: str
    last_updated: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode