import yfinance as yf
import pandas as pd

def create_stock_csv(ticker_obj: yf.Ticker, symbol: str):
    """Fetches company info and saves key fields to stock.csv."""
    print(f"Creating stock.csv for {symbol}...")
    try:
        info = ticker_obj.info
        if not info:
            print(f"  Warning: Could not fetch info for {symbol}. Skipping stock.csv creation.")
            return

        info_df = pd.DataFrame([info])

        stock_cols_available = [
            'symbol', 
            'shortName', 'currency', 'sector', 'industry', 'currentPrice',
            'previousClose', 'regularMarketOpen', 'dayLow', 'dayHigh', 'volume',
            'trailingEps', 'forwardEps', 'trailingPE', 'forwardPE', 'dividendRate',
            'dividendYield', 'bookValue', 'priceToBook', 'priceToSalesTrailing12Months',
            'marketCap', 'enterpriseValue', 'beta', 'trailingPegRatio', 
            'returnOnEquity', 'returnOnAssets', 'profitMargins', 'operatingMargins',
            'revenuePerShare', 'revenueGrowth', 'earningsQuarterlyGrowth',
            'totalDebt', 'totalCash', 'sharesOutstanding'
        ]

        # This assumes 'symbol' is correctly present as a column from the info dictionary.
        stock_df = info_df.reindex(columns=stock_cols_available)

        stock_df.to_csv("stock.csv", index=False)
        print(f"  Successfully created stock.csv for {symbol}.")

    except Exception as e:
        print(f"  An error occurred while creating stock.csv for {symbol}: {e}")


def create_daily_prices_csv(ticker_obj: yf.Ticker, symbol: str):
    """Fetches historical daily prices and saves key fields to daily_prices.csv."""
    print(f"Creating daily_prices.csv for {symbol}...")
    try:
        # Fetch historical data (e.g., for the last 1y available period)
        hist_data = ticker_obj.history(period="1y")

        if hist_data.empty:
            print(f"  Warning: No historical data found for {symbol}. Skipping daily_prices.csv creation.")
            return

        daily_prices_df = hist_data.reset_index()

        daily_prices_cols = [
            'symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'
            
        ]

        # Add the symbol column
        # Use .insert to place it at the beginning
        daily_prices_df.insert(0, 'symbol', symbol)

        # Select and reorder the columns explicitly to ensure order and exclude unwanted ones
        daily_prices_df = daily_prices_df.reindex(columns=daily_prices_cols)

        daily_prices_df.to_csv("daily_prices.csv", index=False)
        print(f"  Successfully created daily_prices.csv for {symbol}.")

    except Exception as e:
        print(f"  An error occurred while creating daily_prices.csv for {symbol}: {e}")


def create_balance_sheet_csv(ticker_obj: yf.Ticker, symbol: str):
    """Fetches balance sheet data and saves key fields to balance_sheet_cleaned.csv."""
    print(f"Creating balance_sheet_cleaned.csv for {symbol}...")
    try:
        balance_sheet = ticker_obj.balance_sheet
        if balance_sheet.empty:
            print(f"  Warning: Could not fetch balance sheet for {symbol}. Skipping balance_sheet_cleaned.csv creation.")
            return

        # Transpose and reset index, renaming the index column to "Date"
        bs_df = balance_sheet.T.reset_index().rename(columns={"index": "Date"})

        # Keeping original yfinance names for financial line items
        balance_sheet_cols_available = [
            'Date', 'Total Assets', 'Total Debt', 'Stockholders Equity', 'Cash And Cash Equivalents'
        ]

        # Add the symbol column
        if 'symbol' not in bs_df.columns:
            bs_df.insert(0, 'symbol', symbol) # Insert symbol at the beginning

        # Select only the available columns, ensuring 'symbol' is included
        final_cols = ['symbol'] + balance_sheet_cols_available
        balance_sheet_cleaned_df = bs_df.reindex(columns=final_cols)

        balance_sheet_cleaned_df.to_csv("balance_sheet_cleaned.csv", index=False)
        print(f"  Successfully created balance_sheet_cleaned.csv for {symbol}.")

    except Exception as e:
        print(f"  An error occurred while creating balance_sheet_cleaned.csv for {symbol}: {e}")


def create_income_statement_csv(ticker_obj: yf.Ticker, symbol: str):
    """Fetches income statement data and saves key fields to income_statement_cleaned.csv."""
    print(f"Creating income_statement_cleaned.csv for {symbol}...")
    try:
        income_stmt = ticker_obj.financials # financials method gets annual income statement
        if income_stmt.empty:
             # Try quarterly if annual is empty
            income_stmt = ticker_obj.quarterly_financials
            if income_stmt.empty:
                print(f"  Warning: Could not fetch income statement (annual or quarterly) for {symbol}. Skipping income_statement_cleaned.csv creation.")
                return

        # Transpose and reset index, renaming the index column to "Date"
        is_df = income_stmt.T.reset_index().rename(columns={"index": "Date"})

        # Keeping original yfinance names for financial line items
        income_statement_cols_available = [
            'Date', 'Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income',
            'Basic EPS', 'Diluted EPS' # Including both Basic and Diluted EPS
        ]

        # Add the symbol column
        if 'symbol' not in is_df.columns:
             is_df.insert(0, 'symbol', symbol) # Insert symbol at the beginning

        # Select only the available columns, ensuring 'symbol' is included
        final_cols = ['symbol'] + income_statement_cols_available
        income_statement_cleaned_df = is_df.reindex(columns=final_cols)

        income_statement_cleaned_df.to_csv("income_statement_cleaned.csv", index=False)
        print(f"  Successfully created income_statement_cleaned.csv for {symbol}.")

    except Exception as e:
        print(f"  An error occurred while creating income_statement_cleaned.csv for {symbol}: {e}")


def create_cash_flow_csv(ticker_obj: yf.Ticker, symbol: str):
    """Fetches cash flow data and saves key fields to cash_flow_cleaned.csv."""
    print(f"Creating cash_flow_cleaned.csv for {symbol}...")
    try:
        cash_flow = ticker_obj.cashflow # cashflow method gets annual cash flow
        if cash_flow.empty:
             # Try quarterly if annual is empty
            cash_flow = ticker_obj.quarterly_cashflow
            if cash_flow.empty:
                print(f"  Warning: Could not fetch cash flow (annual or quarterly) for {symbol}. Skipping cash_flow_cleaned.csv creation.")
                return

        # Transpose and reset index, renaming the index column to "Date"
        cf_df = cash_flow.T.reset_index().rename(columns={"index": "Date"})

        cash_flow_cols_available = [
            'Date', 'Operating Cash Flow', 'Capital Expenditure', 'Free Cash Flow', 'Cash Dividends Paid'
        ]

        # Add the symbol column
        if 'symbol' not in cf_df.columns:
             cf_df.insert(0, 'symbol', symbol) # Insert symbol at the beginning

        # Select only the available columns, ensuring 'symbol' is included
        final_cols = ['symbol'] + cash_flow_cols_available
        cash_flow_cleaned_df = cf_df.reindex(columns=final_cols)

        cash_flow_cleaned_df.to_csv("cash_flow_cleaned.csv", index=False)
        print(f"  Successfully created cash_flow_cleaned.csv for {symbol}.")

    except Exception as e:
        print(f"  An error occurred while creating cash_flow_cleaned.csv for {symbol}: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    STOCK_SYMBOL = "AAPL" # Change this to your desired stock symbol
    apple_ticker = yf.Ticker(STOCK_SYMBOL)

    # Call each function to create the respective CSVs
    create_stock_csv(apple_ticker, STOCK_SYMBOL)
    create_daily_prices_csv(apple_ticker, STOCK_SYMBOL)
    create_balance_sheet_csv(apple_ticker, STOCK_SYMBOL)
    create_income_statement_csv(apple_ticker, STOCK_SYMBOL)
    create_cash_flow_csv(apple_ticker, STOCK_SYMBOL)

    print("\nCSV file creation process finished.") 