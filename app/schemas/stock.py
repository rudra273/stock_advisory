from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal
import math
from datetime import date


class StockInfoResponse(BaseModel):
    symbol: str
    shortName: Optional[str] = None
    currency: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    currentPrice: Optional[float] = None
    previousClose: Optional[float] = None
    regularMarketOpen: Optional[float] = None
    dayLow: Optional[float] = None
    dayHigh: Optional[float] = None
    volume: Optional[float] = None
    trailingEps: Optional[float] = None
    forwardEps: Optional[float] = None
    trailingPE: Optional[float] = None
    forwardPE: Optional[float] = None
    dividendRate: Optional[float] = None
    dividendYield: Optional[float] = None
    bookValue: Optional[float] = None
    priceToBook: Optional[float] = None
    priceToSalesTrailing12Months: Optional[float] = None
    marketCap: Optional[float] = None
    enterpriseValue: Optional[float] = None
    beta: Optional[float] = None
    trailingPegRatio: Optional[float] = None
    returnOnEquity: Optional[float] = None
    returnOnAssets: Optional[float] = None
    profitMargins: Optional[float] = None
    operatingMargins: Optional[float] = None
    revenuePerShare: Optional[float] = None
    revenueGrowth: Optional[float] = None
    earningsQuarterlyGrowth: Optional[float] = None
    totalDebt: Optional[float] = None
    totalCash: Optional[float] = None
    sharesOutstanding: Optional[float] = None

    @field_validator(
        'currentPrice', 'previousClose', 'regularMarketOpen', 'dayLow', 'dayHigh',
        'volume', 'trailingEps', 'forwardEps', 'trailingPE', 'forwardPE',
        'dividendRate', 'dividendYield', 'bookValue', 'priceToBook',
        'priceToSalesTrailing12Months', 'marketCap', 'enterpriseValue', 'beta',
        'trailingPegRatio', 'returnOnEquity', 'returnOnAssets', 'profitMargins',
        'operatingMargins', 'revenuePerShare', 'revenueGrowth',
        'earningsQuarterlyGrowth', 'totalDebt', 'totalCash', 'sharesOutstanding',
        mode='before'
    )
    @classmethod
    def validate_numeric_fields(cls, v):
        if isinstance(v, Decimal) and v.is_nan():
            return None
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    class Config:
        from_attributes = True



class CurrentPriceResponse(BaseModel):
    symbol: str
    companyName: Optional[str] = None
    currentPrice: Optional[float] = None
    previousClose: Optional[float] = None
    Change: Optional[float] = None
    PercentChange: Optional[float] = None

    @field_validator(
        'currentPrice', 'previousClose', 'Change', 'PercentChange',
        mode='before'
    )
    @classmethod
    def validate_float_fields(cls, v):
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    # class Config:
    #     from_attributes = True
    model_config = {"from_attributes": True} 

class DailyPriceResponse(BaseModel):
    symbol: str
    Date: date
    Open: Optional[float] = None
    High: Optional[float] = None
    Low: Optional[float] = None
    Close: Optional[float] = None
    Volume: Optional[float] = None 

    @field_validator(
        'Open', 'High', 'Low', 'Close', 'Volume',
        mode='before'
    )
    @classmethod
    def validate_numeric_fields(cls, v):
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    class Config:
        from_attributes = True

class BalanceSheetResponse(BaseModel):
    symbol: str
    Date: date
    total_assets: Optional[float] = None
    total_debt: Optional[float] = None
    stockholders_equity: Optional[float] = None
    cash_and_cash_equivalents: Optional[float] = None

    @field_validator(
        'total_assets', 'total_debt', 'stockholders_equity', 'cash_and_cash_equivalents',
        mode='before'
    )
    @classmethod
    def validate_decimal_fields(cls, v):
        if isinstance(v, Decimal) and v.is_nan():
            return None
        return v

    class Config:
        from_attributes = True

class IncomeStatementResponse(BaseModel):
    symbol: str
    Date: date
    total_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_income: Optional[float] = None
    net_income: Optional[float] = None
    basic_eps: Optional[float] = None
    diluted_eps: Optional[float] = None

    @field_validator(
        'total_revenue', 'gross_profit', 'operating_income', 'net_income',
        'basic_eps', 'diluted_eps',
        mode='before'
    )
    @classmethod
    def validate_numeric_fields(cls, v):
        if isinstance(v, Decimal) and v.is_nan():
            return None
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    class Config:
        from_attributes = True

class CashFlowResponse(BaseModel):
    symbol: str
    Date: date
    operating_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    free_cash_flow: Optional[float] = None
    cash_dividends_paid: Optional[float] = None

    @field_validator(
        'operating_cash_flow', 'capital_expenditure', 'free_cash_flow', 'cash_dividends_paid',
        mode='before'
    )
    @classmethod
    def validate_decimal_fields(cls, v):
        if isinstance(v, Decimal) and v.is_nan():
            return None
        return v

    class Config:
        from_attributes = True 