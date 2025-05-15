# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

router = APIRouter()

@router.get("/stocks/{symbol}", response_model=Dict[str, Any])
async def get_stock_info(symbol: str):
    try:
        # This is a mock response. Replace with actual data fetching logic
        stock_data = {
            "symbol": symbol,
            "price": 150.25,
            "volume": 1000000,
            "change": 2.5
        }
        return stock_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch stock data: {str(e)}"
        )


