# app/models/base.py
from sqlalchemy import Column, String, Float, BigInteger, Date

from app.db.config import Base

class StockInfo(Base):
    __tablename__ = "stock_info"

    symbol = Column(String, primary_key=True)
    shortName = Column(String)
    currency = Column(String)
    sector = Column(String)
    industry = Column(String)
    currentPrice = Column(Float)
    previousClose = Column(Float)
    regularMarketOpen = Column(Float)
    dayLow = Column(Float)
    dayHigh = Column(Float)
    volume = Column(BigInteger)
    trailingEps = Column(Float)
    forwardEps = Column(Float)
    trailingPE = Column(Float)
    forwardPE = Column(Float)
    dividendRate = Column(Float)
    dividendYield = Column(Float)
    bookValue = Column(Float)
    priceToBook = Column(Float)
    priceToSalesTrailing12Months = Column(Float)
    marketCap = Column(BigInteger)
    enterpriseValue = Column(BigInteger)
    beta = Column(Float)
    trailingPegRatio = Column(Float)
    returnOnEquity = Column(Float)
    returnOnAssets = Column(Float)
    profitMargins = Column(Float)
    operatingMargins = Column(Float)
    revenuePerShare = Column(Float)
    revenueGrowth = Column(Float)
    earningsQuarterlyGrowth = Column(Float)
    totalDebt = Column(BigInteger)
    totalCash = Column(BigInteger)
    sharesOutstanding = Column(BigInteger)



class DailyPrice(Base):
    __tablename__ = "daily_prices"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    Open = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Close = Column(Float)
    Volume = Column(BigInteger)


class BalanceSheet(Base):
    __tablename__ = "balance_sheet"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    Total_Assets = Column("Total Assets", BigInteger)
    Total_Debt = Column("Total Debt", BigInteger)
    Stockholders_Equity = Column("Stockholders Equity", BigInteger)
    Cash_And_Cash_Equivalents = Column("Cash And Cash Equivalents", BigInteger)



class IncomeStatement(Base):
    __tablename__ = "income_statement"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    Total_Revenue = Column("Total Revenue", BigInteger)
    Gross_Profit = Column("Gross Profit", BigInteger)
    Operating_Income = Column("Operating Income", BigInteger)
    Net_Income = Column("Net Income", BigInteger)
    Basic_EPS = Column("Basic EPS", Float)
    Diluted_EPS = Column("Diluted EPS", Float)


class CashFlow(Base):
    __tablename__ = "cash_flow"

    symbol = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    Operating_Cash_Flow = Column("Operating Cash Flow", BigInteger)
    Capital_Expenditure = Column("Capital Expenditure", BigInteger)
    Free_Cash_Flow = Column("Free Cash Flow", BigInteger)
    Cash_Dividends_Paid = Column("Cash Dividends Paid", BigInteger)



class CurrentPrice(Base):
    __tablename__ = "current_prices"

    symbol = Column(String, primary_key=True)
    companyName = Column(String)
    currentPrice = Column(Float)
    previousClose = Column(Float)
    Change = Column(Float)
    PercentChange = Column(Float)
