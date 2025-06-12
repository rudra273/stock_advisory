# app/repositories/stock_kpis.py
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import date

from app.repositories.get_metrics import (
    get_current_price_metrics,
    get_stock_info_metrics,
    get_balance_sheet_metrics,
    get_income_statement_metrics,
    get_cash_flow_metrics
)

from app.repositories.calculated_metrics import (
    calculate_all_ratios,
    calculate_all_technical_indicators
)


def get_metrics_by_category(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Dict[str, Any]]:
    """
    Get all metrics organized by category for better structure.
    
    Args:
        db: Database session
        symbol: Stock symbol (e.g., 'AAPL')
        period_date: Optional specific date for financial statements (uses latest if None)
    
    Returns:
        Dictionary containing all metrics organized by category
    """
    
    # Get current price metrics (from CurrentPrice table)
    current_price_data = get_current_price_metrics(db, symbol)
    
    # Get stock info metrics (excluding current price to avoid duplication)
    stock_info_data = get_stock_info_metrics(db, symbol)
    
    # Get financial statement metrics
    balance_sheet_data = get_balance_sheet_metrics(db, symbol, period_date)
    income_statement_data = get_income_statement_metrics(db, symbol, period_date)
    cash_flow_data = get_cash_flow_metrics(db, symbol, period_date)
    
    # Get calculated ratios
    calculated_ratios = calculate_all_ratios(db, symbol, period_date)
    
    # Get technical indicators
    technical_indicators = calculate_all_technical_indicators(db, symbol)
    

    
    
    # Combine all metrics into categorized dictionary
    return {
        "price_data": {
            "current_price": current_price_data.get("current_price"),
            "previous_close": current_price_data.get("previous_close"),
            "price_change": current_price_data.get("change"),
            "price_change_percent": current_price_data.get("percent_change"),
            "day_low": stock_info_data.get("day_low"),
            "day_high": stock_info_data.get("day_high"),
            "regular_market_open": stock_info_data.get("regular_market_open"),
            "volume": stock_info_data.get("volume")
        },
        
        "company_info": {
            "company_name": current_price_data.get("company_name"),
            "short_name": stock_info_data.get("short_name"),
            "sector": stock_info_data.get("sector"),
            "industry": stock_info_data.get("industry"),
            "currency": stock_info_data.get("currency"),
            "market_cap": stock_info_data.get("market_cap"),
            "enterprise_value": stock_info_data.get("enterprise_value"),
            "shares_outstanding": stock_info_data.get("shares_outstanding"),
            "beta": stock_info_data.get("beta")
        },
        
        "valuation_ratios": {
            "trailing_pe": stock_info_data.get("trailing_pe"),
            "forward_pe": stock_info_data.get("forward_pe"),
            "price_to_book": stock_info_data.get("price_to_book"),
            "price_to_sales": stock_info_data.get("price_to_sales"),
            "trailing_peg_ratio": stock_info_data.get("trailing_peg_ratio"),
            "earnings_yield": calculated_ratios.get("earnings_yield")
        },
        
        "earnings_data": {
            "trailing_eps": stock_info_data.get("trailing_eps"),
            "forward_eps": stock_info_data.get("forward_eps"),
            "basic_eps": income_statement_data.get("basic_eps"),
            "diluted_eps": income_statement_data.get("diluted_eps")
        },
        
        "profitability_ratios": {
            "return_on_equity": stock_info_data.get("return_on_equity"),
            "return_on_assets": stock_info_data.get("return_on_assets"),
            "profit_margins": stock_info_data.get("profit_margins"),
            "operating_margins": stock_info_data.get("operating_margins"),
            "gross_margin": calculated_ratios.get("gross_margin")
        },
        
        "financial_strength": {
            "debt_to_equity": calculated_ratios.get("debt_to_equity"),
            "debt_ratio": calculated_ratios.get("debt_ratio"),
            "asset_turnover": calculated_ratios.get("asset_turnover"),
            "equity_multiplier": calculated_ratios.get("equity_multiplier")
        },
        
        "dividend_data": {
            "dividend_rate": stock_info_data.get("dividend_rate"),
            "dividend_yield": stock_info_data.get("dividend_yield"),
            "payout_ratio": calculated_ratios.get("payout_ratio")
        },
        
        "growth_rates": {
            "revenue_growth": stock_info_data.get("revenue_growth"),
            "earnings_quarterly_growth": stock_info_data.get("earnings_quarterly_growth")
        },
        
        "technical_indicators": {
            "volatility": technical_indicators.get("volatility"),
            "rsi": technical_indicators.get("rsi"),
            "ma_50": technical_indicators.get("moving_averages", {}).get("MA_50"),
            "ma_200": technical_indicators.get("moving_averages", {}).get("MA_200")
        },
        
        "financial_statements": {
            "balance_sheet": {
                "date": balance_sheet_data.get("date"),
                "total_assets": balance_sheet_data.get("total_assets"),
                "total_debt": balance_sheet_data.get("total_debt"),
                "stockholders_equity": balance_sheet_data.get("stockholders_equity"),
                "cash_and_cash_equivalents": balance_sheet_data.get("cash_and_cash_equivalents"),
                "total_cash": stock_info_data.get("total_cash"),
                "book_value": stock_info_data.get("book_value")
            },
            "income_statement": {
                "date": income_statement_data.get("date"),
                "total_revenue": income_statement_data.get("total_revenue"),
                "gross_profit": income_statement_data.get("gross_profit"),
                "operating_income": income_statement_data.get("operating_income"),
                "net_income": income_statement_data.get("net_income"),
                "revenue_per_share": stock_info_data.get("revenue_per_share")
            },
            "cash_flow": {
                "date": cash_flow_data.get("date"),
                "operating_cash_flow": cash_flow_data.get("operating_cash_flow"),
                "capital_expenditure": cash_flow_data.get("capital_expenditure"),
                "free_cash_flow": cash_flow_data.get("free_cash_flow"),
                "cash_dividends_paid": cash_flow_data.get("cash_dividends_paid")
            }
        }
    }

