import os
from app.services.stock.helper import (
    fetch_balance_sheet,
    fetch_cash_flow,
    fetch_daily_prices,
    fetch_income_statement,
    fetch_stock_info,
    fetch_current_prices
)

OUTPUT_DIR = "data/nifty50_csvs"


def ingest_daily_prices():
    df = fetch_daily_prices()
    if df is not None:
        file_path = os.path.join(OUTPUT_DIR, "nifty50_daily_prices.csv")
        try:
            df.to_csv(file_path, index=False)
            print(f"Successfully saved combined daily prices to {file_path}")
        except Exception as e:
            print(f"Error saving daily prices CSV: {e}")
    else:
        print("No daily prices DataFrame to save.")
    return df


def ingest_stock_info():
    df = fetch_stock_info()
    if df is not None:
        file_path = os.path.join(OUTPUT_DIR, "nifty50_stock_info.csv")
        try:
            df.to_csv(file_path, index=False)
            print(f"Successfully saved combined stock info to {file_path}")
        except Exception as e:
            print(f"Error saving stock info CSV: {e}")
    else:
        print("No stock info DataFrame to save.")
    return df


def ingest_balance_sheet():
    df = fetch_balance_sheet()
    if df is not None:
        file_path = os.path.join(OUTPUT_DIR, "nifty50_balance_sheet.csv")
        try:
            df.to_csv(file_path, index=False)
            print(f"Successfully saved combined balance sheet to {file_path}")
        except Exception as e:
            print(f"Error saving balance sheet CSV: {e}")
    else:
        print("No balance sheet DataFrame to save.")
    return df


def ingest_income_statement():
    df = fetch_income_statement()
    if df is not None:
        file_path = os.path.join(OUTPUT_DIR, "nifty50_income_statement.csv")
        try:
            df.to_csv(file_path, index=False)
            print(f"Successfully saved combined income statement to {file_path}")
        except Exception as e:
            print(f"Error saving income statement CSV: {e}")
    else:
        print("No income statement DataFrame to save.")
    return df


def ingest_cash_flow():
    df = fetch_cash_flow()
    if df is not None:
        file_path = os.path.join(OUTPUT_DIR, "nifty50_cash_flow.csv")
        try:
            df.to_csv(file_path, index=False)
            print(f"Successfully saved combined cash flow to {file_path}")
        except Exception as e:
            print(f"Error saving cash flow CSV: {e}")
    else:
        print("No cash flow DataFrame to save.")
    return df


def ingest_current_prices():
    """
    Fetches and saves current price and change data for all Nifty 50 symbols.
    """
    print("\n--- Starting Current Price and Change Ingestion ---")
    df = fetch_current_prices() 
    if df is not None:
        file_path = os.path.join(OUTPUT_DIR, "nifty50_current_prices.csv") # Define the CSV path
        try:
            df.to_csv(file_path, index=False)
            print(f"Successfully saved combined current prices to {file_path}")
        except Exception as e:
            print(f"Error saving current prices CSV: {e}")
    else:
        print("No current prices DataFrame to save.")
    return df

if __name__ == "__main__":
    print("Starting Nifty 50 data fetch process...")

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # Ingest all components
    # ingest_stock_info()
    # ingest_daily_prices()
    # ingest_balance_sheet()
    # ingest_income_statement()
    # ingest_cash_flow()
    ingest_current_prices()

    print("\nNifty 50 data fetch and saving process completed.")


