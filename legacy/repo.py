from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import statistics
from decimal import Decimal

from app.repositories.helper import (
    safe_divide,
    get_latest_financial_data,
    get_previous_period_data
)
from app.models.stock import (
    CurrentPrice,
    StockInfo,
    DailyPrice,
    CashFlow,
    BalanceSheet,
    IncomeStatement
)

from app.repositories.helper import (
    get_current_price_by_symbol,
    get_stock_info_by_symbol,
    get_balance_sheets_by_symbol,
    get_income_statements_by_symbol,
    get_cash_flows_by_symbol,
    get_daily_prices_by_symbol
)

from typing import List, Optional, Dict, Any
from datetime import date, datetime

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


# =============================================================================
# DIRECT DATABASE RETRIEVAL FUNCTIONS (using get_ prefix)
# =============================================================================

# 1. Price-to-Earnings (P/E) Ratio - Available in StockInfo
def get_pe_ratio(db: Session, symbol: str) -> Optional[float]:
    """Get P/E ratio directly from database (trailing P/E)"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.trailingPE if stock_info else None

# 2. Earnings Per Share (EPS) - Available in StockInfo and IncomeStatement
def get_eps(db: Session, symbol: str, use_trailing: bool = True) -> Optional[float]:
    """Get EPS directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    if not stock_info:
        return None
    
    if use_trailing:
        return stock_info.trailingEps
    else:
        return stock_info.forwardEps

# 3. Free Cash Flow - Available in CashFlow table
def get_fcf(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get Free Cash Flow directly from database"""
    cash_flows = get_cash_flows_by_symbol(db, symbol)
    
    if not cash_flows:
        return None
    
    if period_date:
        cash_flow = next((cf for cf in cash_flows if cf.Date == period_date), None)
    else:
        cash_flow = get_latest_financial_data(cash_flows)
    
    return float(cash_flow.free_cash_flow) if cash_flow and cash_flow.free_cash_flow else None

# 4. Return on Equity (ROE) - Available in StockInfo
def get_roe(db: Session, symbol: str) -> Optional[float]:
    """Get ROE directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.returnOnEquity if stock_info else None

# 5. Return on Assets (ROA) - Available in StockInfo
def get_roa(db: Session, symbol: str) -> Optional[float]:
    """Get ROA directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.returnOnAssets if stock_info else None

# 6. Dividend Yield - Available in StockInfo
def get_dividend_yield(db: Session, symbol: str) -> Optional[float]:
    """Get dividend yield directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.dividendYield if stock_info and stock_info.dividendYield else None

# 7. Price-to-Book (P/B) Ratio - Available in StockInfo
def get_pb_ratio(db: Session, symbol: str) -> Optional[float]:
    """Get P/B ratio directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.priceToBook if stock_info else None

# 8. Price-to-Sales (P/S) Ratio - Available in StockInfo
def get_ps_ratio(db: Session, symbol: str) -> Optional[float]:
    """Get P/S ratio directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.priceToSalesTrailing12Months if stock_info else None

# 9. Book Value per Share - Available in StockInfo
def get_bvps(db: Session, symbol: str) -> Optional[float]:
    """Get Book Value per Share directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.bookValue if stock_info else None

# 10. Profit Margins - Available in StockInfo
def get_net_margin(db: Session, symbol: str) -> Optional[float]:
    """Get net profit margin directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.profitMargins * 100 if stock_info and stock_info.profitMargins else None

# 11. Operating Margins - Available in StockInfo
def get_operating_margin(db: Session, symbol: str) -> Optional[float]:
    """Get operating margin directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.operatingMargins * 100 if stock_info and stock_info.operatingMargins else None

# 12. Revenue Growth - Available in StockInfo
def get_revenue_growth(db: Session, symbol: str) -> Optional[float]:
    """Get revenue growth directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.revenueGrowth * 100 if stock_info and stock_info.revenueGrowth else None

# 13. Earnings Growth - Available in StockInfo
def get_earnings_growth(db: Session, symbol: str) -> Optional[float]:
    """Get quarterly earnings growth directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.earningsQuarterlyGrowth * 100 if stock_info and stock_info.earningsQuarterlyGrowth else None

# 14. Revenue Per Share - Available in StockInfo
def get_revenue_per_share(db: Session, symbol: str) -> Optional[float]:
    """Get revenue per share directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.revenuePerShare if stock_info else None

# 15. Beta - Available in StockInfo
def get_beta(db: Session, symbol: str) -> Optional[float]:
    """Get beta directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.beta if stock_info else None

# 16. PEG Ratio - Available in StockInfo
def get_peg_ratio(db: Session, symbol: str) -> Optional[float]:
    """Get PEG ratio directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.trailingPegRatio if stock_info else None

# 17. Market Capitalization - Available in StockInfo
def get_market_cap(db: Session, symbol: str) -> Optional[float]:
    """Get market capitalization directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return float(stock_info.marketCap) if stock_info and stock_info.marketCap else None

# 18. Enterprise Value - Available in StockInfo
def get_enterprise_value(db: Session, symbol: str) -> Optional[float]:
    """Get enterprise value directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return float(stock_info.enterpriseValue) if stock_info and stock_info.enterpriseValue else None

# 19. Forward P/E Ratio - Available in StockInfo
def get_forward_pe(db: Session, symbol: str) -> Optional[float]:
    """Get forward P/E ratio directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.forwardPE if stock_info else None

# 20. Forward EPS - Available in StockInfo
def get_forward_eps(db: Session, symbol: str) -> Optional[float]:
    """Get forward EPS directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.forwardEps if stock_info else None

# 21. Current Stock Price - Available in CurrentPrice or StockInfo
def get_current_price(db: Session, symbol: str) -> Optional[float]:
    """Get current stock price from database"""
    current_price = get_current_price_by_symbol(db, symbol)
    if current_price and current_price.currentPrice:
        return current_price.currentPrice
    
    # Fallback to StockInfo
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.currentPrice if stock_info else None

# 22. Shares Outstanding - Available in StockInfo
def get_shares_outstanding(db: Session, symbol: str) -> Optional[float]:
    """Get shares outstanding directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return float(stock_info.sharesOutstanding) if stock_info and stock_info.sharesOutstanding else None

# 23. Net Income (Period Specific) - Available in IncomeStatement
def get_net_income(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get net income for a specific period from database"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return None
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    return float(income_stmt.net_income) if income_stmt and income_stmt.net_income else None

# 24. Total Revenue (Period Specific) - Available in IncomeStatement
def get_total_revenue(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get total revenue for a specific period from database"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return None
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    return float(income_stmt.total_revenue) if income_stmt and income_stmt.total_revenue else None

# 25. Operating Income (Period Specific) - Available in IncomeStatement
def get_operating_income(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get operating income for a specific period from database"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return None
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    return float(income_stmt.operating_income) if income_stmt and income_stmt.operating_income else None

# 26. Operating Cash Flow (Period Specific) - Available in CashFlow
def get_operating_cash_flow(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get operating cash flow for a specific period from database"""
    cash_flows = get_cash_flows_by_symbol(db, symbol)
    
    if not cash_flows:
        return None
    
    if period_date:
        cash_flow = next((cf for cf in cash_flows if cf.Date == period_date), None)
    else:
        cash_flow = get_latest_financial_data(cash_flows)
    
    return float(cash_flow.operating_cash_flow) if cash_flow and cash_flow.operating_cash_flow else None

# 27. Total Debt - Available in StockInfo or BalanceSheet
def get_total_debt(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get total debt from database"""
    if period_date:
        # Get from balance sheet for specific period
        balance_sheets = get_balance_sheets_by_symbol(db, symbol)
        if balance_sheets:
            balance_sheet = next((bs for bs in balance_sheets if bs.Date == period_date), None)
            if balance_sheet and balance_sheet.total_debt:
                return float(balance_sheet.total_debt)
    
    # Fallback to StockInfo snapshot
    stock_info = get_stock_info_by_symbol(db, symbol)
    return float(stock_info.totalDebt) if stock_info and stock_info.totalDebt else None

# 28. Basic EPS (Period Specific) - Available in IncomeStatement
def get_basic_eps(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get basic EPS for a specific period from database"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return None
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    return income_stmt.basic_eps if income_stmt and income_stmt.basic_eps else None

# 29. Diluted EPS (Period Specific) - Available in IncomeStatement
def get_diluted_eps(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get diluted EPS for a specific period from database"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return None
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    return income_stmt.diluted_eps if income_stmt and income_stmt.diluted_eps else None

# 30. Gross Profit (Period Specific) - Available in IncomeStatement
def get_gross_profit(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get gross profit for a specific period from database"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return None
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    return float(income_stmt.gross_profit) if income_stmt and income_stmt.gross_profit else None

# 31. Total Assets (Period Specific) - Available in BalanceSheet
def get_total_assets(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get total assets for a specific period from database"""
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not balance_sheets:
        return None
    
    if period_date:
        balance_sheet = next((bs for bs in balance_sheets if bs.Date == period_date), None)
    else:
        balance_sheet = get_latest_financial_data(balance_sheets)
    
    return float(balance_sheet.total_assets) if balance_sheet and balance_sheet.total_assets else None

# 32. Stockholders' Equity (Period Specific) - Available in BalanceSheet
def get_stockholders_equity(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get stockholders' equity for a specific period from database"""
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not balance_sheets:
        return None
    
    if period_date:
        balance_sheet = next((bs for bs in balance_sheets if bs.Date == period_date), None)
    else:
        balance_sheet = get_latest_financial_data(balance_sheets)
    
    return float(balance_sheet.stockholders_equity) if balance_sheet and balance_sheet.stockholders_equity else None

# 33. Capital Expenditure (Period Specific) - Available in CashFlow
def get_capital_expenditure(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get capital expenditure for a specific period from database"""
    cash_flows = get_cash_flows_by_symbol(db, symbol)
    
    if not cash_flows:
        return None
    
    if period_date:
        cash_flow = next((cf for cf in cash_flows if cf.Date == period_date), None)
    else:
        cash_flow = get_latest_financial_data(cash_flows)
    
    return float(cash_flow.capital_expenditure) if cash_flow and cash_flow.capital_expenditure else None

# 34. Dividend Rate - Available in StockInfo
def get_dividend_rate(db: Session, symbol: str) -> Optional[float]:
    """Get dividend rate directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return stock_info.dividendRate if stock_info else None

# 35. Total Cash - Available in StockInfo
def get_total_cash(db: Session, symbol: str) -> Optional[float]:
    """Get total cash directly from database"""
    stock_info = get_stock_info_by_symbol(db, symbol)
    return float(stock_info.totalCash) if stock_info and stock_info.totalCash else None

# 36. Cash and Cash Equivalents (Period Specific) - Available in BalanceSheet
def get_cash_equivalents(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get cash and cash equivalents for a specific period from database"""
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not balance_sheets:
        return None
    
    if period_date:
        balance_sheet = next((bs for bs in balance_sheets if bs.Date == period_date), None)
    else:
        balance_sheet = get_latest_financial_data(balance_sheets)
    
    return float(balance_sheet.cash_and_cash_equivalents) if balance_sheet and balance_sheet.cash_and_cash_equivalents else None

# 37. Cash Dividends Paid (Period Specific) - Available in CashFlow
def get_dividends_paid(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Get cash dividends paid for a specific period from database"""
    cash_flows = get_cash_flows_by_symbol(db, symbol)
    
    if not cash_flows:
        return None
    
    if period_date:
        cash_flow = next((cf for cf in cash_flows if cf.Date == period_date), None)
    else:
        cash_flow = get_latest_financial_data(cash_flows)
    
    return float(cash_flow.cash_dividends_paid) if cash_flow and cash_flow.cash_dividends_paid else None

# =============================================================================
# CALCULATED FUNCTIONS (using calculate_ prefix)
# =============================================================================

# 17. Debt-to-Equity Ratio (needs calculation from balance sheet)
def calculate_de_ratio(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate Debt-to-Equity ratio from balance sheet data"""
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not balance_sheets:
        return None
    
    if period_date:
        balance_sheet = next((bs for bs in balance_sheets if bs.Date == period_date), None)
    else:
        balance_sheet = get_latest_financial_data(balance_sheets)
    
    if not balance_sheet or not balance_sheet.total_debt or not balance_sheet.stockholders_equity:
        return None
    
    return safe_divide(balance_sheet.total_debt, balance_sheet.stockholders_equity)

# 18. Earnings Yield (inverse of P/E)
def calculate_earnings_yield(db: Session, symbol: str) -> Optional[float]:
    """Calculate earnings yield (inverse of P/E ratio)"""
    pe_ratio = get_pe_ratio(db, symbol)
    if pe_ratio and pe_ratio > 0:
        return (1 / pe_ratio) * 100
    return None

# 19. Dividend Payout Ratio
def calculate_payout_ratio(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate dividend payout ratio"""
    cash_flows = get_cash_flows_by_symbol(db, symbol)
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not cash_flows or not income_statements:
        return None
    
    if period_date:
        cash_flow = next((cf for cf in cash_flows if cf.Date == period_date), None)
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        cash_flow = get_latest_financial_data(cash_flows)
        income_stmt = get_latest_financial_data(income_statements)
    
    if not cash_flow or not income_stmt or not cash_flow.cash_dividends_paid or not income_stmt.net_income:
        return None
    
    # Convert to positive value (dividends paid is usually negative)
    dividends_paid = abs(float(cash_flow.cash_dividends_paid))
    payout_ratio = safe_divide(dividends_paid, income_stmt.net_income)
    return payout_ratio * 100 if payout_ratio is not None else None

# 20. Debt Ratio
def calculate_debt_ratio(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate debt ratio from balance sheet data"""
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not balance_sheets:
        return None
    
    if period_date:
        balance_sheet = next((bs for bs in balance_sheets if bs.Date == period_date), None)
    else:
        balance_sheet = get_latest_financial_data(balance_sheets)
    
    if not balance_sheet or not balance_sheet.total_debt or not balance_sheet.total_assets:
        return None
    
    return safe_divide(balance_sheet.total_debt, balance_sheet.total_assets)

# 21. Historical Price Volatility
def calculate_volatility(db: Session, symbol: str, days: int = 252) -> Optional[float]:
    """Calculate historical price volatility (standard deviation of returns)"""
    daily_prices = get_daily_prices_by_symbol(db, symbol)
    
    if not daily_prices or len(daily_prices) < 2:
        return None
    
    # Sort by date and take the most recent 'days' entries
    sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
    if len(sorted_prices) > days:
        sorted_prices = sorted_prices[:days]
    
    # Reverse to get chronological order for return calculation
    sorted_prices.reverse()
    
    # Calculate daily returns
    returns = []
    for i in range(1, len(sorted_prices)):
        if sorted_prices[i-1].Close and sorted_prices[i].Close:
            daily_return = (sorted_prices[i].Close - sorted_prices[i-1].Close) / sorted_prices[i-1].Close
            returns.append(daily_return)
    
    if len(returns) < 2:
        return None
    
    # Calculate standard deviation and annualize it
    volatility = statistics.stdev(returns)
    annualized_volatility = volatility * (252 ** 0.5)  # Assuming 252 trading days per year
    return annualized_volatility * 100

# 22. Moving Averages
def calculate_moving_averages(db: Session, symbol: str, periods: List[int] = [50, 200]) -> Dict[str, Optional[float]]:
    """Calculate moving averages for specified periods (default: 50-day and 200-day)"""
    daily_prices = get_daily_prices_by_symbol(db, symbol)
    
    if not daily_prices:
        return {f"MA_{period}": None for period in periods}
    
    # Sort by date (most recent first)
    sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
    
    result = {}
    for period in periods:
        if len(sorted_prices) >= period:
            # Take the most recent 'period' prices
            recent_prices = sorted_prices[:period]
            valid_prices = [price.Close for price in recent_prices if price.Close is not None]
            
            if len(valid_prices) == period:
                ma = sum(valid_prices) / len(valid_prices)
                result[f"MA_{period}"] = ma
            else:
                result[f"MA_{period}"] = None
        else:
            result[f"MA_{period}"] = None
    
    return result

# 23. Asset Turnover (calculated from financial statements)
def calculate_asset_turnover(db: Session, symbol: str, current_date: Optional[date] = None) -> Optional[float]:
    """Calculate asset turnover ratio"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not income_statements or not balance_sheets or len(balance_sheets) < 2:
        return None
    
    if current_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == current_date), None)
        current_bs = next((bs for bs in balance_sheets if bs.Date == current_date), None)
        previous_bs = get_previous_period_data(balance_sheets, current_date)
    else:
        income_stmt = get_latest_financial_data(income_statements)
        sorted_bs = sorted(balance_sheets, key=lambda x: x.Date, reverse=True)
        current_bs = sorted_bs[0]
        previous_bs = sorted_bs[1] if len(sorted_bs) > 1 else None
    
    if not income_stmt or not current_bs or not previous_bs:
        return None
    
    if not income_stmt.total_revenue or not current_bs.total_assets or not previous_bs.total_assets:
        return None
    
    avg_assets = (float(current_bs.total_assets) + float(previous_bs.total_assets)) / 2
    return safe_divide(income_stmt.total_revenue, avg_assets)

# 24. Equity Multiplier
def calculate_equity_multiplier(db: Session, symbol: str, current_date: Optional[date] = None) -> Optional[float]:
    """Calculate equity multiplier"""
    balance_sheets = get_balance_sheets_by_symbol(db, symbol)
    
    if not balance_sheets or len(balance_sheets) < 2:
        return None
    
    if current_date:
        current_bs = next((bs for bs in balance_sheets if bs.Date == current_date), None)
        previous_bs = get_previous_period_data(balance_sheets, current_date)
    else:
        sorted_bs = sorted(balance_sheets, key=lambda x: x.Date, reverse=True)
        current_bs = sorted_bs[0]
        previous_bs = sorted_bs[1] if len(sorted_bs) > 1 else None
    
    if not current_bs or not previous_bs:
        return None
    
    if not current_bs.total_assets or not previous_bs.total_assets or not current_bs.stockholders_equity or not previous_bs.stockholders_equity:
        return None
    
    avg_assets = (float(current_bs.total_assets) + float(previous_bs.total_assets)) / 2
    avg_equity = (float(current_bs.stockholders_equity) + float(previous_bs.stockholders_equity)) / 2
    
    return safe_divide(avg_assets, avg_equity)

# 25. Gross Profit Margin (calculated from income statement)
def calculate_gross_margin(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate gross profit margin from income statement"""
    income_statements = get_income_statements_by_symbol(db, symbol)
    
    if not income_statements:
        return None
    
    if period_date:
        income_stmt = next((stmt for stmt in income_statements if stmt.Date == period_date), None)
    else:
        income_stmt = get_latest_financial_data(income_statements)
    
    if not income_stmt or not income_stmt.gross_profit or not income_stmt.total_revenue:
        return None
    
    margin = safe_divide(income_stmt.gross_profit, income_stmt.total_revenue)
    return margin * 100 if margin is not None else None

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_all_direct_metrics(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Get all metrics that are directly available from database"""
    return {
        # Stock Info Metrics
        "market_cap": get_market_cap(db, symbol),
        "enterprise_value": get_enterprise_value(db, symbol),
        "pe_ratio": get_pe_ratio(db, symbol),
        "forward_pe": get_forward_pe(db, symbol),
        "trailing_eps": get_eps(db, symbol, use_trailing=True),
        "forward_eps": get_forward_eps(db, symbol),
        "current_price": get_current_price(db, symbol),
        "shares_outstanding": get_shares_outstanding(db, symbol),
        "roe": get_roe(db, symbol),
        "roa": get_roa(db, symbol),
        "revenue_growth": get_revenue_growth(db, symbol),
        "operating_margin": get_operating_margin(db, symbol),
        "net_margin": get_net_margin(db, symbol),
        "peg_ratio": get_peg_ratio(db, symbol),
        "dividend_yield": get_dividend_yield(db, symbol),
        "pb_ratio": get_pb_ratio(db, symbol),
        "ps_ratio": get_ps_ratio(db, symbol),
        "book_value_per_share": get_bvps(db, symbol),
        "beta": get_beta(db, symbol),
        "revenue_per_share": get_revenue_per_share(db, symbol),
        "earnings_growth": get_earnings_growth(db, symbol),
        "dividend_rate": get_dividend_rate(db, symbol),
        "total_cash": get_total_cash(db, symbol),
        "total_debt_snapshot": get_total_debt(db, symbol),
        
        # Period-Specific Metrics
        "fcf": get_fcf(db, symbol, period_date),
        "net_income": get_net_income(db, symbol, period_date),
        "total_revenue": get_total_revenue(db, symbol, period_date),
        "operating_income": get_operating_income(db, symbol, period_date),
        "operating_cash_flow": get_operating_cash_flow(db, symbol, period_date),
        "total_debt": get_total_debt(db, symbol, period_date),
        "basic_eps": get_basic_eps(db, symbol, period_date),
        "diluted_eps": get_diluted_eps(db, symbol, period_date),
        "gross_profit": get_gross_profit(db, symbol, period_date),
        "total_assets": get_total_assets(db, symbol, period_date),
        "stockholders_equity": get_stockholders_equity(db, symbol, period_date),
        "capital_expenditure": get_capital_expenditure(db, symbol, period_date),
        "cash_equivalents": get_cash_equivalents(db, symbol, period_date),
        "dividends_paid": get_dividends_paid(db, symbol, period_date)
    }

def calculate_all_computed_metrics(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Calculate all metrics that need computation"""
    return {
        "de_ratio": calculate_de_ratio(db, symbol, period_date),
        "earnings_yield": calculate_earnings_yield(db, symbol),
        "payout_ratio": calculate_payout_ratio(db, symbol, period_date),
        "debt_ratio": calculate_debt_ratio(db, symbol, period_date),
        "volatility": calculate_volatility(db, symbol),
        "asset_turnover": calculate_asset_turnover(db, symbol, period_date),
        "equity_multiplier": calculate_equity_multiplier(db, symbol, period_date),
        "gross_margin": calculate_gross_margin(db, symbol, period_date),
        "moving_averages": calculate_moving_averages(db, symbol)
    }

def get_all_metrics(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Get all available financial metrics for a symbol (both direct and calculated)"""
    direct_metrics = get_all_direct_metrics(db, symbol, period_date)
    calculated_metrics = calculate_all_computed_metrics(db, symbol, period_date)
    
    return {**direct_metrics, **calculated_metrics}

# create a good promt to group all. and clean it.