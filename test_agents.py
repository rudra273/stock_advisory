from datetime import date
from app.db.config import SessionLocal  
from app.agents.search_agent import search_stock_news, search_generic_news, search_google_only
from app.agents.technical_analysis_agent import TechnicalAnalysisAgent


def test():
    db = SessionLocal()
    try:
        symbol = "TCS.NS"
        period_date = date(2025, 3, 31)

       # Initialize with database session
        tech_agent = TechnicalAnalysisAgent(db)
        # Analyze a stock
        result = tech_agent.execute(symbol)

        print(result)
        # Access results
        # print(result["executive_summary"]["sentiment"])  # "Bullish"
        # print(result["executive_summary"]["core_thesis"])  # Dynamic thesis
        # print(result["narrative_analysis"]["bullish_signals"])  # List of bullish signals
        # print(result["data_table"]) 
    finally:
        db.close()

test() 


# Technical Analysis Agent Example Usage
# # In your main application
# from app.agents.technical_analysis_agent import TechnicalAnalysisAgent

# # Initialize with database session
# tech_agent = TechnicalAnalysisAgent(db_session)
# # Analyze a stock
# result = tech_agent.execute("AAPL")

# # Access results
# print(result["executive_summary"]["sentiment"])  # "Bullish"
# print(result["executive_summary"]["core_thesis"])  # Dynamic thesis
# print(result["narrative_analysis"]["bullish_signals"])  # List of bullish signals
# print(result["data_table"])  # Formatted table data



# for the search agent
# if __name__ == "__main__":
    # # 1. Stock search with Google (comprehensive)
    # print("=== Stock Search (With Google) ===")
    # stock_results = search_stock_news("Reliance", use_google=False)
    # print(stock_results)
    # print(f"Query: {stock_results['query']}")
    # print(f"News Org Summary: {stock_results['news_org_summary']}")
    # print(f"Google Summary: {stock_results['google_summary']}")
    # print(f"Overall Summary: {stock_results['overall_summary']}")
    # print(f"Domains: {', '.join(stock_results['sources']['domains'])}")
    
    # # 2. Generic market search with Google
    # print("\n=== Generic Market Search (With Google) ===")
    # market_results = search_generic_news("banking sector analysis", use_google=False)
    # print(market_results)
    # print(f"Query: {market_results['query']}")
    # print(f"News Org Summary: {market_results['news_org_summary']}")
    # print(f"Google Summary: {market_results['google_summary']}")
    # print(f"Overall Summary: {market_results['overall_summary']}")
    # print(f"Domains: {', '.join(market_results['sources']['domains'])}")
    
    # # 3. Google-only search (NEW)
    # print("\n=== Google-Only Search ===")
    # google_results = search_google_only("artificial intelligence trends 2025")
    # print(f"Query: {google_results['query']}")
    # print(f"Summary: {google_results['summary']}")
    # print(f"Domains: {', '.join(google_results['sources']['domains'])}") 