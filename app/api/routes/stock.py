from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.config import get_db
from app.repositories.stock import (
    get_all_current_prices,
    get_current_price_by_symbol,
    get_daily_prices_by_symbol,
    get_all_stock_info,
    get_stock_info_by_symbol,
    get_all_balance_sheets,
    get_balance_sheets_by_symbol,
    get_all_income_statements,
    get_income_statements_by_symbol,
    get_all_cash_flows,
    get_cash_flows_by_symbol,
    get_stock_profile_by_symbol
)
from app.schemas.stock import (
    StockInfoResponse,
    CurrentPriceResponse,
    DailyPriceResponse,
    BalanceSheetResponse,
    IncomeStatementResponse,
    CashFlowResponse
)

router = APIRouter(prefix="/stocks", tags=["Stocks"])

# Get Full stock data of the profile
@router.get("/stock_profile/{symbol}")
def get_stock_profile(symbol: str, db: Session = Depends(get_db)):
    try:
        symbol = symbol.upper()
        profile_data = get_stock_profile_by_symbol(db, symbol)
        
        if not any(profile_data.values()):
            raise HTTPException(status_code=404, detail=f"No data found for symbol '{symbol}'")

        # Convert ORM objects to Pydantic models for response
        return {
            "stock_info": StockInfoResponse.model_validate(profile_data["stock_info"]) if profile_data["stock_info"] else None,
            "current_price": CurrentPriceResponse.model_validate(profile_data["current_price"]) if profile_data["current_price"] else None,
            "balance_sheet": [BalanceSheetResponse.model_validate(bs) for bs in profile_data["balance_sheet"]],
            "income_statement": [IncomeStatementResponse.model_validate(inc) for inc in profile_data["income_statement"]],
            "cash_flow": [CashFlowResponse.model_validate(cf) for cf in profile_data["cash_flow"]]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock profile for '{symbol}': {str(e)}")

# Current price APIs
@router.get("/current-prices", response_model=List[CurrentPriceResponse])
def api_get_current_prices(db: Session = Depends(get_db)):
    try:
        prices = get_all_current_prices(db)
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch current prices: {str(e)}")

@router.get("/current-prices/{symbol}", response_model=CurrentPriceResponse)
def api_get_current_price(symbol: str, db: Session = Depends(get_db)):
    try:
        stock = get_current_price_by_symbol(db, symbol)
        if not stock:
            raise HTTPException(status_code=404, detail=f"Current price for symbol '{symbol}' not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch current price for '{symbol}': {str(e)}")

# Daily Price APIs (Returns 1yr data of Specific Stock)
@router.get("/daily-prices/{symbol}", response_model=List[DailyPriceResponse])
def api_get_daily_prices(symbol: str, db: Session = Depends(get_db)):
    try:
        records = get_daily_prices_by_symbol(db, symbol)
        if not records:
            raise HTTPException(status_code=404, detail=f"No daily price data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch daily prices for '{symbol}': {str(e)}")

@router.get("/stock-info", response_model=List[StockInfoResponse])
def api_get_stock_info_list(db: Session = Depends(get_db)):
    try:
        stocks = get_all_stock_info(db)
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock info list: {str(e)}")

@router.get("/stock-info/{symbol}", response_model=StockInfoResponse)
def api_get_stock_info(symbol: str, db: Session = Depends(get_db)):
    try:
        stock = get_stock_info_by_symbol(db, symbol)
        if not stock:
            raise HTTPException(status_code=404, detail=f"Stock info for symbol '{symbol}' not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock info for '{symbol}': {str(e)}")

# BalanceSheet APIs
@router.get("/balance-sheet", response_model=List[BalanceSheetResponse])
def api_get_balance_sheets(db: Session = Depends(get_db)):
    try:
        records = get_all_balance_sheets(db)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch balance sheet data: {str(e)}")

@router.get("/balance-sheet/{symbol}", response_model=List[BalanceSheetResponse])
def api_get_balance_sheet(symbol: str, db: Session = Depends(get_db)):
    try:
        records = get_balance_sheets_by_symbol(db, symbol)
        if not records:
            raise HTTPException(status_code=404, detail=f"No balance sheet data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch balance sheet for '{symbol}': {str(e)}")

# IncomeStatement APIs
@router.get("/income-statement", response_model=List[IncomeStatementResponse])
def api_get_income_statements(db: Session = Depends(get_db)):
    try:
        records = get_all_income_statements(db)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income statement data: {str(e)}")

@router.get("/income-statement/{symbol}", response_model=List[IncomeStatementResponse])
def api_get_income_statement(symbol: str, db: Session = Depends(get_db)):
    try:
        records = get_income_statements_by_symbol(db, symbol)
        if not records:
            raise HTTPException(status_code=404, detail=f"No income statement data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income statement for '{symbol}': {str(e)}")

# CashFlow APIs
@router.get("/cash-flow", response_model=List[CashFlowResponse])
def api_get_cash_flows(db: Session = Depends(get_db)):
    try:
        records = get_all_cash_flows(db)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cash flow data: {str(e)}")

@router.get("/cash-flow/{symbol}", response_model=List[CashFlowResponse])
def api_get_cash_flow(symbol: str, db: Session = Depends(get_db)):
    try:
        records = get_cash_flows_by_symbol(db, symbol)
        if not records:
            raise HTTPException(status_code=404, detail=f"No cash flow data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cash flow for '{symbol}': {str(e)}")
    
