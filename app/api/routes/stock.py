from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.config import get_db
from app.models.stock import CurrentPrice

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/current-prices")
def get_current_prices(db: Session = Depends(get_db)):
    return db.query(CurrentPrice).all()
