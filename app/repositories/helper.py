# app/repositories/helper.py
from typing import List, Optional
from datetime import date
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


def safe_divide(numerator, denominator):
    """Safely divide two numbers, return None if denominator is 0 or None"""
    if denominator is None or denominator == 0:
        return None
    if numerator is None:
        return None
    return float(numerator) / float(denominator)


def get_latest_financial_data(statements: List, date_field: str = 'Date'):
    """Get the most recent financial statement from a list"""
    if not statements:
        return None
    return max(statements, key=lambda x: getattr(x, date_field))


def get_previous_period_data(statements: List, current_date: date, date_field: str = 'Date'):
    """Get the previous period's financial statement"""
    if not statements or len(statements) < 2:
        return None
    
    # Sort by date descending
    sorted_statements = sorted(statements, key=lambda x: getattr(x, date_field), reverse=True)
    
    # Find current period and return the next one (previous chronologically)
    for i, stmt in enumerate(sorted_statements):
        if getattr(stmt, date_field) == current_date and i + 1 < len(sorted_statements):
            return sorted_statements[i + 1]
    return None


def format_large_number(value: Optional[float], unit: str = "") -> str:
    """Format large numbers with appropriate suffixes (K, M, B, T)"""
    if value is None:
        return "N/A"
    
    if abs(value) >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T {unit}".strip()
    elif abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B {unit}".strip()
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M {unit}".strip()
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K {unit}".strip()
    else:
        return f"{value:.2f} {unit}".strip()


def format_percentage(value: Optional[float], decimal_places: int = 2) -> str:
    """Format percentage values"""
    if value is None:
        return "N/A"
    return f"{value:.{decimal_places}f}%"


def format_currency(value: Optional[float], currency: str = "$", decimal_places: int = 2) -> str:
    """Format currency values"""
    if value is None:
        return "N/A"
    return f"{currency}{value:,.{decimal_places}f}"


# ========================================================================================================


# get metrics funtion.


# Function to get all current prices
def get_all_current_prices(db: Session) -> List[CurrentPrice]:
    return db.query(CurrentPrice).all()

# Function to get current price by symbol
def get_current_price_by_symbol(db: Session, symbol: str) -> Optional[CurrentPrice]:
    return db.query(CurrentPrice).filter(CurrentPrice.symbol == symbol.upper()).first()

# Function to get daily prices by symbol for 1 yr 
# def get_daily_prices_by_symbol(db: Session, symbol: str) -> List[DailyPrice]:
#     return db.query(DailyPrice).filter(DailyPrice.symbol == symbol.upper()).all()

def get_daily_prices_by_symbol(db: Session, symbol: str, limit: Optional[int] = None) -> List[DailyPrice]:
 
    # Start the query and filter by the symbol
    query = db.query(DailyPrice).filter(DailyPrice.symbol == symbol.upper())
    
    # CRITICAL: Always sort by date in descending order to get the latest prices first
    query = query.order_by(DailyPrice.Date.desc())
    
    # Apply the limit if it was provided
    if limit:
        query = query.limit(limit)
        
    return query.all()


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

