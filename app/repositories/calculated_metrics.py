# app/repositories/calculated_metrics.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import statistics

from app.repositories.helper import (
    get_balance_sheets_by_symbol,
    get_income_statements_by_symbol,
    get_cash_flows_by_symbol,
    get_daily_prices_by_symbol,
    safe_divide,
    get_latest_financial_data,
    get_previous_period_data
)


from app.repositories.get_metrics import (
    get_stock_info_metrics,
    get_balance_sheet_metrics,
    get_income_statement_metrics,
    get_cash_flow_metrics
)


# =============================================================================
# CALCULATED FINANCIAL RATIOS
# =============================================================================

def calculate_de_ratio(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate Debt-to-Equity ratio from balance sheet data"""
    balance_sheet = get_balance_sheet_metrics(db, symbol, period_date)
    
    total_debt = balance_sheet.get("total_debt")
    stockholders_equity = balance_sheet.get("stockholders_equity")
    
    if not total_debt or not stockholders_equity:
        return None
    
    return safe_divide(total_debt, stockholders_equity)


def calculate_earnings_yield(db: Session, symbol: str) -> Optional[float]:
    """Calculate earnings yield (inverse of P/E ratio)"""
    stock_info = get_stock_info_metrics(db, symbol)
    pe_ratio = stock_info.get("trailing_pe")
    
    if pe_ratio and pe_ratio > 0:
        return (1 / pe_ratio) * 100
    return None


def calculate_payout_ratio(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate dividend payout ratio"""
    cash_flow = get_cash_flow_metrics(db, symbol, period_date)
    income_statement = get_income_statement_metrics(db, symbol, period_date)
    
    dividends_paid = cash_flow.get("cash_dividends_paid")
    net_income = income_statement.get("net_income")
    
    if not dividends_paid or not net_income:
        return None
    
    # Convert to positive value (dividends paid is usually negative)
    dividends_paid = abs(dividends_paid)
    payout_ratio = safe_divide(dividends_paid, net_income)
    return payout_ratio * 100 if payout_ratio is not None else None


def calculate_debt_ratio(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate debt ratio from balance sheet data"""
    balance_sheet = get_balance_sheet_metrics(db, symbol, period_date)
    
    total_debt = balance_sheet.get("total_debt")
    total_assets = balance_sheet.get("total_assets")
    
    if not total_debt or not total_assets:
        return None
    
    return safe_divide(total_debt, total_assets)


def calculate_gross_margin(db: Session, symbol: str, period_date: Optional[date] = None) -> Optional[float]:
    """Calculate gross profit margin from income statement"""
    income_statement = get_income_statement_metrics(db, symbol, period_date)
    
    gross_profit = income_statement.get("gross_profit")
    total_revenue = income_statement.get("total_revenue")
    
    if not gross_profit or not total_revenue:
        return None
    
    margin = safe_divide(gross_profit, total_revenue)
    return margin * 100 if margin is not None else None


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


# =============================================================================
# TECHNICAL ANALYSIS METRICS
# =============================================================================

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


def calculate_rsi(db: Session, symbol: str, periods: int = 14) -> Optional[float]:
    """Calculate Relative Strength Index (RSI)"""
    daily_prices = get_daily_prices_by_symbol(db, symbol)
    
    if not daily_prices or len(daily_prices) < periods + 1:
        return None
    
    # Sort by date (most recent first) and take needed periods + 1
    sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)[:periods + 1]
    sorted_prices.reverse()  # Chronological order for calculation
    
    gains = []
    losses = []
    
    for i in range(1, len(sorted_prices)):
        if sorted_prices[i-1].Close and sorted_prices[i].Close:
            change = sorted_prices[i].Close - sorted_prices[i-1].Close
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
    
    if len(gains) < periods:
        return None
    
    avg_gain = sum(gains[-periods:]) / periods
    avg_loss = sum(losses[-periods:]) / periods
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def calculate_all_ratios(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Calculate all financial ratios"""
    return {
        "debt_to_equity": calculate_de_ratio(db, symbol, period_date),
        "earnings_yield": calculate_earnings_yield(db, symbol),
        "payout_ratio": calculate_payout_ratio(db, symbol, period_date),
        "debt_ratio": calculate_debt_ratio(db, symbol, period_date),
        "gross_margin": calculate_gross_margin(db, symbol, period_date),
        "asset_turnover": calculate_asset_turnover(db, symbol, period_date),
        "equity_multiplier": calculate_equity_multiplier(db, symbol, period_date)
    }


def calculate_all_technical_indicators(db: Session, symbol: str) -> Dict[str, Any]:
    """Calculate all technical analysis indicators"""
    return {
        "volatility": calculate_volatility(db, symbol),
        "moving_averages": calculate_moving_averages(db, symbol),
        "rsi": calculate_rsi(db, symbol)
    }


def calculate_all_metrics(db: Session, symbol: str, period_date: Optional[date] = None) -> Dict[str, Any]:
    """Calculate all computed metrics (ratios and technical indicators)"""
    ratios = calculate_all_ratios(db, symbol, period_date)
    technical = calculate_all_technical_indicators(db, symbol)
    
    return {**ratios, **technical}