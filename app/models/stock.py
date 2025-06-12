# app/models/base.py
from sqlalchemy import Column, String, Float, BigInteger, Date, Numeric
from app.db.config import Base



class CurrentPrice(Base):
    __tablename__ = "current_prices"

    symbol = Column(String, primary_key=True)
    companyName = Column(String)
    currentPrice = Column(Float)
    previousClose = Column(Float)
    Change = Column(Float)
    PercentChange = Column(Float)


class DailyPrice(Base):
    __tablename__ = "daily_prices"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    Open = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Close = Column(Float)
    Volume = Column(BigInteger)


class StockInfo(Base):
    __tablename__ = "stock_info"

    symbol = Column(String, primary_key=True)
    shortName = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    currentPrice = Column(Float, nullable=True)
    previousClose = Column(Float, nullable=True)
    regularMarketOpen = Column(Float, nullable=True)
    dayLow = Column(Float, nullable=True)
    dayHigh = Column(Float, nullable=True)
    volume = Column(BigInteger, nullable=True)
    trailingEps = Column(Float, nullable=True)
    forwardEps = Column(Float, nullable=True)
    trailingPE = Column(Float, nullable=True)
    forwardPE = Column(Float, nullable=True)
    dividendRate = Column(Float, nullable=True)
    dividendYield = Column(Float, nullable=True)
    bookValue = Column(Float, nullable=True)
    priceToBook = Column(Float, nullable=True)
    priceToSalesTrailing12Months = Column(Float, nullable=True)
    marketCap = Column(Numeric(38, 0), nullable=True)
    enterpriseValue = Column(Numeric(38, 0), nullable=True)
    beta = Column(Float, nullable=True)
    trailingPegRatio = Column(Float, nullable=True)
    returnOnEquity = Column(Float, nullable=True)
    returnOnAssets = Column(Float, nullable=True)
    profitMargins = Column(Float, nullable=True)
    operatingMargins = Column(Float, nullable=True)
    revenuePerShare = Column(Float, nullable=True)
    revenueGrowth = Column(Float, nullable=True)
    earningsQuarterlyGrowth = Column(Float, nullable=True)
    totalDebt = Column(Numeric(38, 0), nullable=True)
    totalCash = Column(Numeric(38, 0), nullable=True)
    sharesOutstanding = Column(Numeric(38, 0), nullable=True)


class BalanceSheet(Base):
    __tablename__ = "balance_sheet"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    total_assets = Column(Numeric(38, 2), nullable=True)
    total_debt = Column(Numeric(38, 2), nullable=True)
    stockholders_equity = Column(Numeric(38, 2), nullable=True)
    cash_and_cash_equivalents = Column(Numeric(38, 2), nullable=True)


class IncomeStatement(Base):
    __tablename__ = "income_statement"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    total_revenue = Column(Numeric(38, 2), nullable=True)
    gross_profit = Column(Numeric(38, 2), nullable=True)
    operating_income = Column(Numeric(38, 2), nullable=True)
    net_income = Column(Numeric(38, 2), nullable=True)
    basic_eps = Column(Float, nullable=True)
    diluted_eps = Column(Float, nullable=True)


class CashFlow(Base):
    __tablename__ = "cash_flow"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    operating_cash_flow = Column(Numeric(38, 2), nullable=True)
    capital_expenditure = Column(Numeric(38, 2), nullable=True)
    free_cash_flow = Column(Numeric(38, 2), nullable=True)
    cash_dividends_paid = Column(Numeric(38, 2), nullable=True)