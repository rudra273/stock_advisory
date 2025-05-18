import yfinance as yf
import pandas as pd

def stock(symbol: str) -> pd.DataFrame | None:
    """Fetches company info for a given symbol and returns a DataFrame with key fields."""
    print(f"Fetching stock info for {symbol}...")
    try:
        ticker_obj = yf.Ticker(symbol) # Instantiate Ticker inside the function
        info = ticker_obj.info
        if not info:
            print(f"  Warning: Could not fetch info for {symbol}. Returning None.")
            return None

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

        # stock_df.to_csv("stock.csv", index=False) # Commented out as requested
        print(f"  Successfully fetched stock info for {symbol}.")
        return stock_df

    except Exception as e:
        print(f"  An error occurred while fetching stock info for {symbol}: {e}")
        return None


def daily_prices(symbol: str) -> pd.DataFrame | None:
    """Fetches historical daily prices for a given symbol and returns a DataFrame with key fields."""
    print(f"Fetching daily prices for {symbol}...")
    try:
        ticker_obj = yf.Ticker(symbol) 
        # Fetch historical data (e.g., for the last 1y available period)
        hist_data = ticker_obj.history(period="1y")

        if hist_data.empty:
            print(f"  Warning: No historical data found for {symbol}. Returning None.")
            return None

        daily_prices_df = hist_data.reset_index()

        daily_prices_cols = [
            'symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'

        ]

        # Add the symbol column
        # Use .insert to place it at the beginning
        daily_prices_df.insert(0, 'symbol', symbol)

        # Select and reorder the columns explicitly to ensure order and exclude unwanted ones
        daily_prices_df = daily_prices_df.reindex(columns=daily_prices_cols)

        # daily_prices_df.to_csv("daily_prices.csv", index=False) # Commented out as requested
        print(f"  Successfully fetched daily prices for {symbol}.")
        return daily_prices_df

    except Exception as e:
        print(f"  An error occurred while fetching daily prices for {symbol}: {e}")
        return None


def balance_sheet(symbol: str) -> pd.DataFrame | None:
    """Fetches balance sheet data for a given symbol and returns a DataFrame with key fields."""
    print(f"Fetching balance sheet for {symbol}...")
    try:
        ticker_obj = yf.Ticker(symbol) # Instantiate Ticker inside the function
        balance_sheet_data = ticker_obj.balance_sheet
        if balance_sheet_data.empty:
            print(f"  Warning: Could not fetch balance sheet for {symbol}. Returning None.")
            return None

        # Transpose and reset index, renaming the index column to "Date"
        bs_df = balance_sheet_data.T.reset_index().rename(columns={"index": "Date"})

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

        # balance_sheet_cleaned_df.to_csv("balance_sheet_cleaned.csv", index=False) # Commented out as requested
        print(f"  Successfully fetched balance sheet for {symbol}.")
        return balance_sheet_cleaned_df

    except Exception as e:
        print(f"  An error occurred while fetching balance sheet for {symbol}: {e}")
        return None


def income_statement(symbol: str) -> pd.DataFrame | None:
    """Fetches income statement data for a given symbol and returns a DataFrame with key fields."""
    print(f"Fetching income statement for {symbol}...")
    try:
        ticker_obj = yf.Ticker(symbol) # Instantiate Ticker inside the function
        income_stmt_data = ticker_obj.financials # financials method gets annual income statement
        if income_stmt_data.empty:
             # Try quarterly if annual is empty
            income_stmt_data = ticker_obj.quarterly_financials
            if income_stmt_data.empty:
                print(f"  Warning: Could not fetch income statement (annual or quarterly) for {symbol}. Returning None.")
                return None

        # Transpose and reset index, renaming the index column to "Date"
        is_df = income_stmt_data.T.reset_index().rename(columns={"index": "Date"})

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

        # income_statement_cleaned_df.to_csv("income_statement_cleaned.csv", index=False) # Commented out as requested
        print(f"  Successfully fetched income statement for {symbol}.")
        return income_statement_cleaned_df

    except Exception as e:
        print(f"  An error occurred while fetching income statement for {symbol}: {e}")
        return None


def cash_flow(symbol: str) -> pd.DataFrame | None:
    """Fetches cash flow data for a given symbol and returns a DataFrame with key fields."""
    print(f"Fetching cash flow for {symbol}...")
    try:
        ticker_obj = yf.Ticker(symbol) # Instantiate Ticker inside the function
        cash_flow_data = ticker_obj.cashflow
        if cash_flow_data.empty:
             # Try quarterly if annual is empty
            cash_flow_data = ticker_obj.quarterly_cashflow
            if cash_flow_data.empty:
                print(f"  Warning: Could not fetch cash flow (annual or quarterly) for {symbol}. Returning None.")
                return None

        # Transpose and reset index, renaming the index column to "Date"
        cf_df = cash_flow_data.T.reset_index().rename(columns={"index": "Date"})

        cash_flow_cols_available = [
            'Date', 'Operating Cash Flow', 'Capital Expenditure', 'Free Cash Flow', 'Cash Dividends Paid'
        ]

        # Add the symbol column
        if 'symbol' not in cf_df.columns:
             cf_df.insert(0, 'symbol', symbol) # Insert symbol at the beginning

        # Select only the available columns, ensuring 'symbol' is included
        final_cols = ['symbol'] + cash_flow_cols_available
        cash_flow_cleaned_df = cf_df.reindex(columns=final_cols)

        # cash_flow_cleaned_df.to_csv("cash_flow_cleaned.csv", index=False) # Commented out as requested
        print(f"  Successfully fetched cash flow for {symbol}.")
        return cash_flow_cleaned_df

    except Exception as e:
        print(f"  An error occurred while fetching cash flow for {symbol}: {e}")
        return None
    


def current(symbol: str) -> pd.DataFrame | None:
    """
    Fetches current price and previous close for a symbol to calculate daily change.

    Returns a DataFrame with symbol, companyName, currentPrice, previousClose,
    Change, and PercentChange columns, with Change and PercentChange rounded to 2 decimal places.
    """
    print(f"Fetching current price and change for {symbol}...")
    try:
        ticker_obj = yf.Ticker(symbol)
        info = ticker_obj.info

        # Ensure essential keys are present
        if not info or info.get('currentPrice') is None or info.get('previousClose') is None or info.get('shortName') is None:
            print(f"  Warning: Could not fetch essential price info or name for {symbol}. Returning None.")
            return None

        current_price = info.get('currentPrice')
        previous_close = info.get('previousClose')
        short_name = info.get('shortName')

        change = None
        percent_change = None

        # Calculate Change if possible
        if current_price is not None and previous_close is not None:
             change = current_price - previous_close

        # Calculate Percent Change if possible
        if previous_close is not None and previous_close != 0 and current_price is not None:
             percent_change = ((current_price - previous_close) / previous_close) * 100


        data = {
            'symbol': [symbol],
            'companyName': [short_name],
            'currentPrice': [current_price],
            'previousClose': [previous_close],
            'Change': [change], 
            'PercentChange': [percent_change] 
        }

        result_df = pd.DataFrame(data)

        if 'Change' in result_df.columns:
             result_df['Change'] = result_df['Change'].round(2)

        if 'PercentChange' in result_df.columns:
             result_df['PercentChange'] = result_df['PercentChange'].round(2)
        # ---------------------------------------------------------

        print(f"  Successfully fetched current price and change for {symbol}.")
        return result_df

    except Exception as e:
        print(f"  An error occurred while fetching current price and change for {symbol}: {e}")
        return None


# # --- Main Execution ---
# if __name__ == "__main__":
#     STOCK_SYMBOL = "AAPL" # Change this to your desired stock symbol

#     print(f"Processing data for {STOCK_SYMBOL}...")

#     # Call each function with the symbol string to get the DataFrames
#     stock_df_result = stock(STOCK_SYMBOL)
#     daily_prices_df_result = daily_prices(STOCK_SYMBOL)
#     balance_sheet_df_result = balance_sheet(STOCK_SYMBOL)
#     income_statement_df_result = income_statement(STOCK_SYMBOL)
#     cash_flow_df_result = cash_flow(STOCK_SYMBOL)
