from sqlalchemy.orm import Session
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
        with next(get_db()) as db:
            db.query(CashFlow).delete()
            db.bulk_insert_mappings(CashFlow, df.to_dict(orient="records"))
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
