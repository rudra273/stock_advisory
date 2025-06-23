from sqlalchemy.orm import Session
import pandas as pd
from app.db.config import get_db
from app.models.stock import (
    StockInfo, BalanceSheet, IncomeStatement,
    CashFlow, DailyPrice, CurrentPrice
)
from app.services.stock.helper import (
    fetch_stock_info, fetch_balance_sheet,
    fetch_income_statement, fetch_cash_flow,
    fetch_daily_prices, fetch_current_prices
)

from app.models.market_sentiment import MarketSentiment
from app.services.crawler.market_index import fear_greed_index, mmi


def ingest_stock_info():
    df = fetch_stock_info()
    if df is not None and not df.empty:
        with next(get_db()) as db:
            db.query(StockInfo).delete()
            db.bulk_insert_mappings(StockInfo, df.to_dict(orient="records"))
            db.commit()
            print("Stock info ingested successfully.")


def ingest_balance_sheet():
    df = fetch_balance_sheet()
    if df is not None and not df.empty:
        with next(get_db()) as db:
            db.query(BalanceSheet).delete()
            db.bulk_insert_mappings(BalanceSheet, df.to_dict(orient="records"))
            db.commit()
            print("Balance sheet ingested successfully.")


def ingest_income_statement():
    df = fetch_income_statement()
    if df is not None and not df.empty:
        with next(get_db()) as db:
            db.query(IncomeStatement).delete()
            db.bulk_insert_mappings(IncomeStatement, df.to_dict(orient="records"))
            db.commit()
            print("Income statement ingested successfully.")



def ingest_cash_flow():
    df = fetch_cash_flow() 
    if df is not None and not df.empty:
        records = df.to_dict(orient="records")  
        with next(get_db()) as db:
            db.query(CashFlow).delete()
            db.bulk_insert_mappings(CashFlow, records)
            db.commit()
            print("Cash flow ingested successfully.") 

def ingest_daily_prices():
    df = fetch_daily_prices()
    if df is not None and not df.empty:
        with next(get_db()) as db:
            db.query(DailyPrice).delete()
            db.bulk_insert_mappings(DailyPrice, df.to_dict(orient="records"))
            db.commit()
            print("Daily prices ingested successfully.")


def ingest_current_prices():
    df = fetch_current_prices()
    if df is not None and not df.empty:
        with next(get_db()) as db:
            db.query(CurrentPrice).delete()
            db.bulk_insert_mappings(CurrentPrice, df.to_dict(orient="records"))
            db.commit()
            print("Current prices ingested successfully.")


# ...existing code...


def ingest_market_sentiment():
    # Ingest CNN Fear & Greed Index
    cnn_data = fear_greed_index()
    if cnn_data:
        with next(get_db()) as db:
            db.query(MarketSentiment).filter(MarketSentiment.source == "CNN Fear & Greed Index").delete()
            db.add(MarketSentiment(
                source="CNN Fear & Greed Index",
                score=cnn_data['score'],
                rating=cnn_data['rating'],
                last_updated=cnn_data['last_updated']
            ))
            db.commit()
            print("CNN Fear & Greed Index ingested successfully.")

    # Ingest Market Mood Index
    mmi_data = mmi()
    if mmi_data:
        with next(get_db()) as db:
            db.query(MarketSentiment).filter(MarketSentiment.source == "Tickertape Market Mood Index").delete()
            db.add(MarketSentiment(
                source="Tickertape Market Mood Index",
                score=mmi_data['score'],
                rating=mmi_data['rating'],
                last_updated=mmi_data['last_updated']
            ))
            db.commit()
            print("Market Mood Index ingested successfully.")
