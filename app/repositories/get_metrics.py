# app/repositories/get_metrics.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import date, datetime


from app.repositories.helper import (
    get_current_price_by_symbol,
    get_stock_info_by_symbol,
    get_balance_sheets_by_symbol,
    get_income_statements_by_symbol,
    get_cash_flows_by_symbol,
    get_daily_prices_by_symbol,
    get_latest_financial_data,
    get_previous_period_data
)


def get_current_price_metrics(db: Session, symbol: str) -> Dict[str, Any]:
    """Get all current price related metrics from CurrentPrice table"""
    current_price = get_current_price_by_symbol(db, symbol)
    
    if not current_price:
        return {
            "current_price": None,
            "previous_close": None,
            "change": None,
            "percent_change": None,
            "company_name": None
        }
    
    return {
        "current_price": current_price.currentPrice,
        "previous_close": current_price.previousClose,
        "change": current_price.Change,
        "percent_change": current_price.PercentChange,
        "company_name": current_price.companyName
    }


def get_stock_info_metrics(db: Session, symbol: str) -> Dict[str, Any]:
    """Get all stock info metrics from StockInfo table"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    
    if not stock_info:
        return {
            "short_name": None,
            "currency": None,
            "sector": None,
            "industry": None,
            "previous_close": None,
            "regular_market_open": None,
            "day_low": None,
            "day_high": None,
            "volume": None,
            "trailing_eps": None,
            "forward_eps": None,
            "trailing_pe": None,
            "forward_pe": None,
            "dividend_rate": None,
            "dividend_yield": None,
            "book_value": None,
            "price_to_book": None,
            "price_to_sales": None,
            "market_cap": None,
            "enterprise_value": None,
            "beta": None,
            "trailing_peg_ratio": None,
            "return_on_equity": None,
            "return_on_assets": None,
            "profit_margins": None,
            "operating_margins": None,
            "revenue_per_share": None,
            "revenue_growth": None,
            "earnings_quarterly_growth": None,
            "total_debt": None,
            "total_cash": None,
            "shares_outstanding": None
        }
    
    return {
        "short_name": stock_info.shortName,
        "currency": stock_info.currency,
        "sector": stock_info.sector,
        "industry": stock_info.industry,
        "previous_close": stock_info.previousClose,
        "regular_market_open": stock_info.regularMarketOpen,
        "day_low": stock_info.dayLow,
        "day_high": stock_info.dayHigh,
        "volume": int(stock_info.volume) if stock_info.volume else None,
        "trailing_eps": stock_info.trailingEps,
        "forward_eps": stock_info.forwardEps,
        "trailing_pe": stock_info.trailingPE,
        "forward_pe": stock_info.forwardPE,
        "dividend_rate": stock_info.dividendRate,
        "dividend_yield": stock_info.dividendYield * 100 if stock_info.dividendYield else None,
        "book_value": stock_info.bookValue,
        "price_to_book": stock_info.priceToBook,
        "price_to_sales": stock_info.priceToSalesTrailing12Months,
        "market_cap": float(stock_info.marketCap) if stock_info.marketCap else None,
        "enterprise_value": float(stock_info.enterpriseValue) if stock_info.enterpriseValue else None,
        "beta": stock_info.beta,
        "trailing_peg_ratio": stock_info.trailingPegRatio,
        "return_on_equity": stock_info.returnOnEquity * 100 if stock_info.returnOnEquity else None,
        "return_on_assets": stock_info.returnOnAssets * 100 if stock_info.returnOnAssets else None,
        "profit_margins": stock_info.profitMargins * 100 if stock_info.profitMargins else None,
        "operating_margins": stock_info.operatingMargins * 100 if stock_info.operatingMargins else None,
        "revenue_per_share": stock_info.revenuePerShare,
        "revenue_growth": stock_info.revenueGrowth * 100 if stock_info.revenueGrowth else None,
        "earnings_quarterly_growth": stock_info.earningsQuarterlyGrowth * 100 if stock_info.earningsQuarterlyGrowth else None,
        "total_debt": float(stock_info.totalDebt) if stock_info.totalDebt else None,
        "total_cash": float(stock_info.totalCash) if stock_info.totalCash else None,
        "shares_outstanding": float(stock_info.sharesOutstanding) if stock_info.sharesOutstanding else None
    }


def get_balance_sheet_metrics(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Get balance sheet metrics for a specific period"""
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not balance_sheets:
        return {
            "date": None,
            "total_assets": None,
            "total_debt": None,
            "stockholders_equity": None,
            "cash_and_cash_equivalents": None
        }
    
    if period_date:
        balance_sheet = next((bs for bs in balance_sheets if bs.Date == period_date), None)
    else:
        balance_sheet = get_latest_financial_data(balance_sheets)
    
    if not balance_sheet:
        return {
            "date": None,
            "total_assets": None,
            "total_debt": None,
            "stockholders_equity": None,
            "cash_and_cash_equivalents": None
        }
    
    return {
        "date": balance_sheet.Date,
        "total_assets": float(balance_sheet.total_assets) if balance_sheet.total_assets else None,
        "total_debt": float(balance_sheet.total_debt) if balance_sheet.total_debt else None,
        "stockholders_equity": float(balance_sheet.stockholders_equity) if balance_sheet.stockholders_equity else None,
        "cash_and_cash_equivalents": float(balance_sheet.cash_and_cash_equivalents) if balance_sheet.cash_and_cash_equivalents else None
    }


def get_income_statement_metrics(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Get income statement metrics for a specific period"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return {
            "date": None,
            "total_revenue": None,
            "gross_profit": None,
            "operating_income": None,
            "net_income": None,
            "basic_eps": None,
            "diluted_eps": None
        }
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    if not income_stmt:
        return {
            "date": None,
            "total_revenue": None,
            "gross_profit": None,
            "operating_income": None,
            "net_income": None,
            "basic_eps": None,
            "diluted_eps": None
        }
    
    return {
        "date": income_stmt.Date,
        "total_revenue": float(income_stmt.total_revenue) if income_stmt.total_revenue else None,
        "gross_profit": float(income_stmt.gross_profit) if income_stmt.gross_profit else None,
        "operating_income": float(income_stmt.operating_income) if income_stmt.operating_income else None,
        "net_income": float(income_stmt.net_income) if income_stmt.net_income else None,
        "basic_eps": income_stmt.basic_eps,
        "diluted_eps": income_stmt.diluted_eps
    }


def get_cash_flow_metrics(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Get cash flow metrics for a specific period"""
    cash_flows = get_cash_flows_by_symbol(db, symbol)
    
    if not cash_flows:
        return {
            "date": None,
            "operating_cash_flow": None,
            "capital_expenditure": None,
            "free_cash_flow": None,
            "cash_dividends_paid": None
        }
    
    if period_date:
        cash_flow = next((cf for cf in cash_flows if cf.Date == period_date), None)
    else:
        cash_flow = get_latest_financial_data(cash_flows)
    
    if not cash_flow:
        return {
            "date": None,
            "operating_cash_flow": None,
            "capital_expenditure": None,
            "free_cash_flow": None,
            "cash_dividends_paid": None
        }
    
    return {
        "date": cash_flow.Date,
        "operating_cash_flow": float(cash_flow.operating_cash_flow) if cash_flow.operating_cash_flow else None,
        "capital_expenditure": float(cash_flow.capital_expenditure) if cash_flow.capital_expenditure else None,
        "free_cash_flow": float(cash_flow.free_cash_flow) if cash_flow.free_cash_flow else None,
        "cash_dividends_paid": float(cash_flow.cash_dividends_paid) if cash_flow.cash_dividends_paid else None
    }


def get_daily_prices_metrics(db: Session, symbol: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get daily price metrics (useful for technical analysis)"""
    daily_prices = get_daily_prices_by_symbol(db, symbol)
    
    if not daily_prices:
        return []
    
    # Sort by date descending (most recent first)
    sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
    
    if limit:
        sorted_prices = sorted_prices[:limit]
    
    return [
        {
            "date": price.Date,
            "open": price.Open,
            "high": price.High,
            "low": price.Low,
            "close": price.Close,
            "volume": int(price.Volume) if price.Volume else None
        }
        for price in sorted_prices
    ]

