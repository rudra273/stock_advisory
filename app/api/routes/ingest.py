from fastapi import APIRouter
from app.tasks.ingestor import (
    ingest_daily_prices,
    ingest_current_prices,
    ingest_stock_info,
    ingest_balance_sheet,
    ingest_income_statement,
    ingest_cash_flow,
)

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/daily")
def trigger_daily_prices():
    df = ingest_daily_prices()
    return {"message": "Daily prices ingestion triggered", "rows": len(df) if df is not None else 0}

@router.post("/current")
def trigger_current_prices():
    df = ingest_current_prices()
    return {"message": "Current prices ingestion triggered", "rows": len(df) if df is not None else 0}

@router.post("/stock-info")
def trigger_stock_info_ingestion():
    df = ingest_stock_info()
    return {"message": "Stock info ingestion triggered", "rows": len(df) if df is not None else 0}

@router.post("/balance-sheet")
def trigger_balance_sheet_ingestion():
    df = ingest_balance_sheet()
    return {"message": "Balance sheet ingestion triggered", "rows": len(df) if df is not None else 0}

@router.post("/income-statement")
def trigger_income_statement_ingestion():
    df = ingest_income_statement()
    return {"message": "Income statement ingestion triggered", "rows": len(df) if df is not None else 0}

@router.post("/cash-flow")
def trigger_cash_flow_ingestion():
    df = ingest_cash_flow()
    return {"message": "Cash flow ingestion triggered", "rows": len(df) if df is not None else 0}

