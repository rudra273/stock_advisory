from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.stock import (
    CurrentPrice, 
    StockInfo, 
    DailyPrice, 
    CashFlow, 
    BalanceSheet, 
    IncomeStatement
)

# Function to get all current prices
def get_all_current_prices(db: Session) -> List[CurrentPrice]:
    return db.query(CurrentPrice).all()

# Function to get current price by symbol
def get_current_price_by_symbol(db: Session, symbol: str) -> Optional[CurrentPrice]:
    return db.query(CurrentPrice).filter(CurrentPrice.symbol == symbol.upper()).first()

# Function to get daily prices by symbol
def get_daily_prices_by_symbol(db: Session, symbol: str) -> List[DailyPrice]:
    return db.query(DailyPrice).filter(DailyPrice.symbol == symbol.upper()).all()

# Function to get all stock info
def get_all_stock_info(db: Session) -> List[StockInfo]:
    return db.query(StockInfo).all()

# Function to get stock info by symbol
def get_stock_info_by_symbol(db: Session, symbol: str) -> Optional[StockInfo]:
    return db.query(StockInfo).filter(StockInfo.symbol == symbol.upper()).first()

# Function to get all balance sheets
def get_all_balance_sheets(db: Session) -> List[BalanceSheet]:
    return db.query(BalanceSheet).all()

# Function to get balance sheets by symbol
def get_balance_sheets_by_symbol(db: Session, symbol: str) -> List[BalanceSheet]:
    return db.query(BalanceSheet).filter(BalanceSheet.symbol == symbol.upper()).all()

# Function to get all income statements
def get_all_income_statements(db: Session) -> List[IncomeStatement]:
    return db.query(IncomeStatement).all()

# Function to get income statements by symbol
def get_income_statements_by_symbol(db: Session, symbol: str) -> List[IncomeStatement]:
    return db.query(IncomeStatement).filter(IncomeStatement.symbol == symbol.upper()).all()

# Function to get all cash flows
def get_all_cash_flows(db: Session) -> List[CashFlow]:
    return db.query(CashFlow).all()

# Function to get cash flows by symbol
def get_cash_flows_by_symbol(db: Session, symbol: str) -> List[CashFlow]:
    return db.query(CashFlow).filter(CashFlow.symbol == symbol.upper()).all()

# Function to get complete stock profile
def get_stock_profile_by_symbol(db: Session, symbol: str) -> dict:
    symbol = symbol.upper()
    
    stock_info = get_stock_info_by_symbol(db, symbol)
    current_price = get_current_price_by_symbol(db, symbol)
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    income_statements = get_income_statements_by_symbol(db, symbol)
    cash_flows = get_cash_flows_by_symbol(db, symbol)
    
    return {
        "stock_info": stock_info,
        "current_price": current_price,
        "balance_sheet": balance_sheets,
        "income_statement": income_statements,
        "cash_flow": cash_flows
    }

