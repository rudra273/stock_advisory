import yfinance as yf
import pandas as pd

# Choose your stock symbol
ticker_symbol = "AAPL"
ticker = yf.Ticker(ticker_symbol)

# 1. Company Info
info = ticker.info
info_df = pd.DataFrame([info])
info_df.to_csv("info.csv", index=False)

# 2. Balance Sheet
balance_sheet = ticker.balance_sheet
bs_df = balance_sheet.T.reset_index().rename(columns={"index": "Date"})
bs_df.to_csv("balance_sheet.csv", index=False)

# 3. Income Statement
income_stmt = ticker.financials
is_df = income_stmt.T.reset_index().rename(columns={"index": "Date"})
is_df.to_csv("income_statement.csv", index=False)

# 4. Cash Flow Statement
cash_flow = ticker.cashflow
cf_df = cash_flow.T.reset_index().rename(columns={"index": "Date"})
cf_df.to_csv("cash_flow.csv", index=False)

# Print columns of each CSV for inspection
print("INFO COLUMNS:\n", info_df.columns.tolist())
print("\nBALANCE SHEET COLUMNS:\n", bs_df.columns.tolist())
print("\nINCOME STATEMENT COLUMNS:\n", is_df.columns.tolist())
print("\nCASH FLOW COLUMNS:\n", cf_df.columns.tolist())
