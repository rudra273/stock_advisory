# app/tasks/ingestor.py
import pandas as pd
from typing import List, Optional 
import os
from app.services.stock import yfinance_api
# import yfinance_api


# List of Nifty 50 symbols
nifty50_symbols: List[str] = [
    'ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BEL.NS', 'BHARTIARTL.NS',
    'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ETERNAL.NS',
    'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS',
    'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS',
    'ITC.NS', 'JIOFIN.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS',
    'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS',
    'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SHRIRAMFIN.NS', 'SBIN.NS',
    'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS',
    'TECHM.NS', 'TITAN.NS', 'TRENT.NS', 'ULTRACEMCO.NS', 'WIPRO.NS'
]

OUTPUT_DIR = "data/nifty50_csvs"

def fetch_stock_info() -> Optional[pd.DataFrame]:
    """
    Fetches general stock information for all Nifty 50 symbols and returns a DataFrame.
    Returns None if yfinance_api is not available or no data is collected.
    """
    if yfinance_api is None:
        print("yfinance_api is not available. Cannot ingest stock info.")
        return None

    all_stock_info_dfs: List[pd.DataFrame] = []

    for symbol in nifty50_symbols:
        df = yfinance_api.stock(symbol)
        if df is not None and not df.empty:
            all_stock_info_dfs.append(df)
        else:
            print(f"  Skipping {symbol} for stock info (no data).")

    if not all_stock_info_dfs:
        print("No stock info data collected for any symbol.")
        return None # Return None if no data was collected

    combined_df = pd.concat(all_stock_info_dfs, ignore_index=True)
    print("Stock info ingestion complete.")
    return combined_df


def fetch_daily_prices() -> Optional[pd.DataFrame]:
    """
    Fetches daily historical prices for all Nifty 50 symbols and returns a DataFrame.
    Returns None if yfinance_api is not available or no data is collected.
    """
    if yfinance_api is None:
        print("yfinance_api is not available. Cannot ingest daily prices.")
        return None

    all_daily_prices_dfs: List[pd.DataFrame] = []

    for symbol in nifty50_symbols:
        df = yfinance_api.daily_prices(symbol)
        if df is not None and not df.empty:
            all_daily_prices_dfs.append(df)
        else:
            print(f"  Skipping {symbol} for daily prices (no data).")

    if not all_daily_prices_dfs:
        print("No daily prices data collected for any symbol.")
        return None 

    combined_df = pd.concat(all_daily_prices_dfs, ignore_index=True)
    print("Daily prices ingestion complete.")
    return combined_df


def fetch_balance_sheet() -> Optional[pd.DataFrame]:
    """
    Fetches balance sheet data for all Nifty 50 symbols and returns a DataFrame.
    Returns None if yfinance_api is not available or no data is collected.
    """
    if yfinance_api is None:
        print("yfinance_api is not available. Cannot ingest balance sheet.")
        return None

    all_balance_sheet_dfs: List[pd.DataFrame] = []

    for symbol in nifty50_symbols:
        df = yfinance_api.balance_sheet(symbol)
        if df is not None and not df.empty:
            all_balance_sheet_dfs.append(df)
        else:
            print(f"  Skipping {symbol} for balance sheet (no data).")

    if not all_balance_sheet_dfs:
        print("No balance sheet data collected for any symbol.")
        return None

    combined_df = pd.concat(all_balance_sheet_dfs, ignore_index=True)
    print("Balance sheet ingestion complete.")
    return combined_df


def fetch_income_statement() -> Optional[pd.DataFrame]:
    """
    Fetches income statement data for all Nifty 50 symbols and returns a DataFrame.
    Returns None if yfinance_api is not available or no data is collected.
    """
    if yfinance_api is None:
        print("yfinance_api is not available. Cannot ingest income statement.")
        return None

    all_income_statement_dfs: List[pd.DataFrame] = []

    for symbol in nifty50_symbols:
        df = yfinance_api.income_statement(symbol)
        if df is not None and not df.empty:
            all_income_statement_dfs.append(df)
        else:
            print(f"  Skipping {symbol} for income statement (no data).")

    if not all_income_statement_dfs:
        print("No income statement data collected for any symbol.")
        return None # Return None if no data was collected

    # Ensure consistent columns before concatenating if possible
    combined_df = pd.concat(all_income_statement_dfs, ignore_index=True)
    print("Income statement ingestion complete.")
    return combined_df


def fetch_cash_flow() -> Optional[pd.DataFrame]:
    """
    Fetches cash flow data for all Nifty 50 symbols and returns a DataFrame.
    Returns None if yfinance_api is not available or no data is collected.
    """
    if yfinance_api is None:
        print("yfinance_api is not available. Cannot ingest cash flow.")
        return None

    all_cash_flow_dfs: List[pd.DataFrame] = []

    for symbol in nifty50_symbols:
        df = yfinance_api.cash_flow(symbol)
        if df is not None and not df.empty:
            all_cash_flow_dfs.append(df)
        else:
            print(f"  Skipping {symbol} for cash flow (no data).")

    if not all_cash_flow_dfs:
        print("No cash flow data collected for any symbol.")
        return None # Return None if no data was collected

    # Ensure consistent columns before concatenating if possible
    combined_df = pd.concat(all_cash_flow_dfs, ignore_index=True)
    print("Cash flow ingestion complete.")
    return combined_df


def fetch_current_prices() -> Optional[pd.DataFrame]:
    """
    Fetches current price and change data for all Nifty 50 symbols and returns a combined DataFrame.
    Returns None if yfinance_api is not available or no data is collected.
    """
    if yfinance_api is None:
        print("yfinance_api is not available. Cannot ingest current prices.")
        return None

    all_current_price_dfs: List[pd.DataFrame] = []

    for symbol in nifty50_symbols:
        df = yfinance_api.current(symbol)
        if df is not None and not df.empty:
            all_current_price_dfs.append(df)
        else:
            print(f"  Skipping {symbol} for current price (no data or error).")

    if not all_current_price_dfs:
        print("No current price or change data collected for any symbol.")
        return None 

    # Concatenate all collected DataFrames
    combined_df = pd.concat(all_current_price_dfs, ignore_index=True)
    print("Current price and change ingestion complete.")
    return combined_df


# # --- Main Execution Block ---
# if __name__ == "__main__":
#     print("Starting Nifty 50 data fetch process...")

#     # Create output directory if it doesn't exist
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)
#         print(f"Created output directory: {OUTPUT_DIR}")

#     # --- Fetch and Save Stock Info ---
#     stock_info_df = fetch_stock_info()
#     if stock_info_df is not None:
#         file_path = os.path.join(OUTPUT_DIR, 'nifty50_stock_info.csv')
#         try:
#             stock_info_df.to_csv(file_path, index=False)
#             print(f"Successfully saved combined stock info to {file_path}")
#         except Exception as e:
#             print(f"Error saving stock info CSV: {e}")
#     else:
#         print("No stock info DataFrame to save.")

#     # --- Fetch and Save Daily Prices ---
#     daily_prices_df = fetch_daily_prices()
#     if daily_prices_df is not None:
#         file_path = os.path.join(OUTPUT_DIR, 'nifty50_daily_prices.csv')
#         try:
#             daily_prices_df.to_csv(file_path, index=False)
#             print(f"Successfully saved combined daily prices to {file_path}")
#         except Exception as e:
#             print(f"Error saving daily prices CSV: {e}")
#     else:
#         print("No daily prices DataFrame to save.")

#     # --- Fetch and Save Balance Sheet ---
#     balance_sheet_df = fetch_balance_sheet()
#     if balance_sheet_df is not None:
#         file_path = os.path.join(OUTPUT_DIR, 'nifty50_balance_sheet.csv')
#         try:
#             balance_sheet_df.to_csv(file_path, index=False)
#             print(f"Successfully saved combined balance sheet to {file_path}")
#         except Exception as e:
#             print(f"Error saving balance sheet CSV: {e}")
#     else:
#         print("No balance sheet DataFrame to save.")

#     # --- Fetch and Save Income Statement ---
#     income_statement_df = fetch_income_statement()
#     if income_statement_df is not None:
#         file_path = os.path.join(OUTPUT_DIR, 'nifty50_income_statement.csv')
#         try:
#             income_statement_df.to_csv(file_path, index=False)
#             print(f"Successfully saved combined income statement to {file_path}")
#         except Exception as e:
#             print(f"Error saving income statement CSV: {e}")
#     else:
#         print("No income statement DataFrame to save.")

#     # --- Fetch and Save Cash Flow ---
#     cash_flow_df = fetch_cash_flow()
#     if cash_flow_df is not None:
#         file_path = os.path.join(OUTPUT_DIR, 'nifty50_cash_flow.csv')
#         try:
#             cash_flow_df.to_csv(file_path, index=False)
#             print(f"Successfully saved combined cash flow to {file_path}")
#         except Exception as e:
#             print(f"Error saving cash flow CSV: {e}")
#     else:
#         print("No cash flow DataFrame to save.")

#     print("\nNifty 50 data fetch and saving process completed.") 
