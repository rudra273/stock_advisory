# old api which directly intract with db.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.config import get_db
from app.models.stock import CurrentPrice, StockInfo, DailyPrice, CashFlow, BalanceSheet, IncomeStatement
from typing import List, Optional
from app.schemas.stock import (
    StockInfoResponse,
    CurrentPriceResponse,
    DailyPriceResponse,
    BalanceSheetResponse,
    IncomeStatementResponse,
    CashFlowResponse
)


router = APIRouter(prefix="/stocks", tags=["Stocks"])


# get Full stock data of the profile..
@router.get("/stock_profile/{symbol}")
def get_stock_profile(symbol: str, db: Session = Depends(get_db)):
    try:
        symbol = symbol.upper()

        stock_info = db.query(StockInfo).filter(StockInfo.symbol == symbol).first()
        current_price = db.query(CurrentPrice).filter(CurrentPrice.symbol == symbol).first()
        balance_sheets = db.query(BalanceSheet).filter(BalanceSheet.symbol == symbol).all()
        income_statements = db.query(IncomeStatement).filter(IncomeStatement.symbol == symbol).all()
        cash_flows = db.query(CashFlow).filter(CashFlow.symbol == symbol).all()

        if not any([stock_info, current_price, balance_sheets, income_statements, cash_flows]):
            raise HTTPException(status_code=404, detail=f"No data found for symbol '{symbol}'")

        # Correct Pydantic v2 serialization for ORM objects
        # Simply pass the ORM object to the Pydantic model constructor
        # Pydantic will use from_attributes=True from the Config to map the fields
        return {
            "stock_info": StockInfoResponse.model_validate(stock_info) if stock_info else None,
            "current_price": CurrentPriceResponse.model_validate(current_price) if current_price else None,
            "balance_sheet": [BalanceSheetResponse.model_validate(bs) for bs in balance_sheets],
            "income_statement": [IncomeStatementResponse.model_validate(inc) for inc in income_statements],
            "cash_flow": [CashFlowResponse.model_validate(cf) for cf in cash_flows]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock profile for '{symbol}': {str(e)}")


# Current price APIs
@router.get("/current-prices", response_model=List[CurrentPriceResponse])
def get_current_prices(db: Session = Depends(get_db)):
    try:
        prices = db.query(CurrentPrice).all()
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch current prices: {str(e)}") 

@router.get("/current-prices/{symbol}", response_model=CurrentPriceResponse)
def get_current_price(symbol: str, db: Session = Depends(get_db)):
    try:
        stock = db.query(CurrentPrice).filter(CurrentPrice.symbol == symbol.upper()).first()
        if not stock:
            raise HTTPException(status_code=404, detail=f"Current price for symbol '{symbol}' not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch current price for '{symbol}': {str(e)}")


# Daily Price APIs ( Returns 1yr data of Specific Stock)
@router.get("/daily-prices/{symbol}", response_model=List[DailyPriceResponse])
def get_daily_prices(symbol: str, db: Session = Depends(get_db)):
    try:
        records = db.query(DailyPrice).filter(DailyPrice.symbol == symbol.upper()).all()
        if not records:
            raise HTTPException(status_code=404, detail=f"No daily price data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch daily prices for '{symbol}': {str(e)}")


@router.get("/stock-info", response_model=List[StockInfoResponse])
def get_stock_info_list(db: Session = Depends(get_db)):
    try:
        stocks = db.query(StockInfo).all()
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock info list: {str(e)}")


@router.get("/stock-info/{symbol}", response_model=StockInfoResponse)
def get_stock_info(symbol: str, db: Session = Depends(get_db)):
    try:
        stock = db.query(StockInfo).filter(StockInfo.symbol == symbol.upper()).first()
        if not stock:
            raise HTTPException(status_code=404, detail=f"Stock info for symbol '{symbol}' not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock info for '{symbol}': {str(e)}")


# BalanceSheet APIs
@router.get("/balance-sheet", response_model=List[BalanceSheetResponse])
def get_balance_sheets(db: Session = Depends(get_db)):
    try:
        records = db.query(BalanceSheet).all()
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch balance sheet data: {str(e)}")

@router.get("/balance-sheet/{symbol}", response_model=List[BalanceSheetResponse])
def get_balance_sheet(symbol: str, db: Session = Depends(get_db)):
    try:
        records = db.query(BalanceSheet).filter(BalanceSheet.symbol == symbol.upper()).all()
        if not records:
            raise HTTPException(status_code=404, detail=f"No balance sheet data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch balance sheet for '{symbol}': {str(e)}")


# IncomeStatement APIs
@router.get("/income-statement", response_model=List[IncomeStatementResponse])
def get_income_statements(db: Session = Depends(get_db)):
    try:
        records = db.query(IncomeStatement).all()
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income statement data: {str(e)}")

@router.get("/income-statement/{symbol}", response_model=List[IncomeStatementResponse])
def get_income_statement(symbol: str, db: Session = Depends(get_db)):
    try:
        records = db.query(IncomeStatement).filter(IncomeStatement.symbol == symbol.upper()).all()
        if not records:
            raise HTTPException(status_code=404, detail=f"No income statement data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income statement for '{symbol}': {str(e)}")


# CashFlow APIs
@router.get("/cash-flow", response_model=List[CashFlowResponse])
def get_cash_flows(db: Session = Depends(get_db)):
    try:
        records = db.query(CashFlow).all()
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cash flow data: {str(e)}")

@router.get("/cash-flow/{symbol}", response_model=List[CashFlowResponse])
def get_cash_flow(symbol: str, db: Session = Depends(get_db)):
    try:
        records = db.query(CashFlow).filter(CashFlow.symbol == symbol.upper()).all()
        if not records:
            raise HTTPException(status_code=404, detail=f"No cash flow data found for symbol '{symbol}'")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cash flow for '{symbol}': {str(e)}")
