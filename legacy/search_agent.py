# app/agents/search_agent.py

from typing import Dict, List, Any, Optional
from app.agents.base import BaseAgent
from app.services.llm.gemini_llm import GeminiLLM
from app.services.search.news_org import fetch_news, fetch_indian_news
from app.services.search.google import google_search
from app.services.crawler.scraper import scrape_google_results

class SearchAgent(BaseAgent):
    """Search agent for stock-related news and information"""
    
    def __init__(self):
        self.llm = GeminiLLM()
        self.llm_instance = self.llm.get_llm()
    
    def execute(self, query: str, use_google: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Stock-specific search for news and information
        
        Args:
            query: Search query (company name)
            use_google: Whether to include Google search results
            
        Returns:
            Dictionary with stock-specific analysis
        """
        results = {
            "query": query,
            "specific_news": [],
            "google_news": [],
            "news_org_summary": "",
            "google_summary": "",
            "overall_summary": "",
            "sources": {
                "urls": [],
                "domains": [],
                "api_sources": []
            }
        }
        
        # 1. Get specific stock news from Indian sources
        specific_news = self._get_specific_news(query)
        results["specific_news"] = specific_news
        
        # 2. Create batch summary for news_org articles
        if specific_news:
            results["news_org_summary"] = self._create_batch_summary(specific_news, "news_org", query)
        
        # 3. Optional Google search
        if use_google:
            google_news = self._get_google_news(f"{query} stock")
            results["google_news"] = google_news
            
            # 4. Create batch summary for Google articles
            if google_news:
                results["google_summary"] = self._create_batch_summary(google_news, "google", query)
        
        # 5. Generate overall summary using both batch summaries
        results["overall_summary"] = self._generate_final_summary(results, query, "stock")
        
        # 6. Collect all sources in structured format
        source_info = self._collect_all_sources_structured(results, use_google)
        results["sources"].update(source_info)
        
        return results

    def search_generic_news(self, query: str, use_google: bool = False) -> Dict[str, Any]:
        """
        Generic search for market queries like 'top 10 Indian stocks', 'market trends' etc.
        
        Args:
            query: Generic market query
            use_google: Whether to include Google search results
            
        Returns:
            Dictionary with market information
        """
        results = {
            "query": query,
            "news_results": [],
            "google_results": [],
            "news_org_summary": "",
            "google_summary": "",
            "overall_summary": "",
            "sources": {
                "urls": [],
                "domains": [],
                "api_sources": []
            }
        }
        
        # 1. Search news for the generic query
        news_data = fetch_news(query=query, limit=15)
        results["news_results"] = news_data
        
        # 2. Create batch summary for news_org articles
        if news_data:
            results["news_org_summary"] = self._create_batch_summary(news_data, "news_org", query)
        
        # 3. Search Google for additional information (if requested)
        if use_google:
            google_news = self._get_google_news(query)
            results["google_results"] = google_news
            
            # 4. Create batch summary for Google articles
            if google_news:
                results["google_summary"] = self._create_batch_summary(google_news, "google", query)
        
        # 5. Generate overall summary using both batch summaries
        results["overall_summary"] = self._generate_final_summary(results, query, "generic")
        
        # 6. Collect all sources in structured format
        source_info = self._collect_all_sources_structured(results, use_google)
        results["sources"].update(source_info)
        
        return results

    def _get_specific_news(self, query: str) -> List[Dict]:
        """Fetch specific news for the given query"""
        try:
            return fetch_indian_news(query=query, limit=10)
        except Exception as e:
            print(f"Error fetching specific news for '{query}': {e}")
            return []

    def _get_google_news(self, query: str) -> List[Dict]:
        """Fetch and scrape Google search results"""
        try:
            # Search Google for stock-related query
            search_query = f"{query} stock news India"
            google_results = google_search(search_query)
            
            # Take top 5 results
            top_results = google_results[:5]
            
            # Scrape the URLs
            scraped_results = scrape_google_results(top_results, max_words=500)
            
            # Convert scraped results to news format
            google_news = []
            for result in scraped_results:
                if result['status'] == 'success':
                    news_item = {
                        'title': result['title'],
                        'description': result['content'][:200] + '...' if len(result['content']) > 200 else result['content'],
                        'content': result['content'],
                        'url': result['url'],
                        'source_name': self._extract_domain(result['url'])
                    }
                    google_news.append(news_item)
            
            return google_news
        except Exception as e:
            print(f"Error fetching Google news for '{query}': {e}")
            return []

    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return "Unknown"


    def _create_batch_summary(self, news_list: List[Dict], source_type: str, query: str) -> str:
        """Create a single summary for all articles from a source"""
        if not news_list:
            return ""
        
        # Combine all articles into one text
        combined_text = ""
        for i, news in enumerate(news_list, 1):
            title = news.get('title', 'N/A')
            description = news.get('description', '')
            content = news.get('content', '')
            
            article_text = f"Article {i}: {title}"
            if description:
                article_text += f" - {description}"
            if content and content != description:
                article_text += f" {content}"
            
            combined_text += article_text + "\n\n"
        
        # Create appropriate prompt based on source type
        if source_type == "news_org":
            prompt = f"""
            Summarize the following news articles about "{query}" from Indian news sources:
            
            {combined_text}
            
            Create a comprehensive summary focusing on key developments, market trends, financial performance, 
            company announcements, and overall market impact. Adapt the focus based on whether this is about 
            a specific company, sector, or broader market topic.
            """
        else:  # google
            prompt = f"""
            Summarize the following articles from Google search results about "{query}":
            
            {combined_text}
            
            Create a comprehensive summary covering the main points and developments.
            """
        
        try:
            response = self.llm_instance.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            print(f"Error creating batch summary for {source_type}: {e}")
            return f"Summary of {len(news_list)} articles from {source_type} sources about {query}"

    def _generate_final_summary(self, results: Dict, query: str, search_type: str) -> str:
        """Generate final overall summary using batch summaries"""
        news_org_summary = results.get("news_org_summary", "")
        google_summary = results.get("google_summary", "")
        
        # Get the appropriate key names based on search type
        if search_type == "stock":
            news_key = "specific_news"
            google_key = "google_news"
        else:
            news_key = "news_results"
            google_key = "google_results"
        
        news_count = len(results.get(news_key, []))
        google_count = len(results.get(google_key, []))
        
        if not news_org_summary and not google_summary:
            return f"No relevant information found for '{query}'"
        
        prompt = f"""
        Based on the following research about "{query}", create a final comprehensive summary:
        
        """
        
        if news_org_summary:
            prompt += f"""
        News Sources Summary ({news_count} articles):
        {news_org_summary}
        
        """
        
        if google_summary:
            prompt += f"""
        Additional Research Summary ({google_count} articles):
        {google_summary}
        
        """
        
        if search_type == "stock":
            prompt += f"""
        Provide a comprehensive analysis of {query} covering key developments, recent announcements, market performance, and overall outlook based on the available information.
        """
        else:
            prompt += f"""
        Provide a comprehensive market analysis for "{query}" covering current trends, key insights, market implications, and overall outlook based on the available information.
        """
        
        try:
            response = self.llm_instance.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            print(f"Error generating final summary: {e}")
            total_articles = news_count + google_count
            return f"Analysis for '{query}': Found {total_articles} relevant articles covering recent developments and market information."

    def _collect_all_sources_structured(self, results: Dict, use_google: bool = False) -> Dict[str, List[str]]:
        """
        Single function to collect all sources in structured format for ANY results dictionary
        Works for both execute() and search_generic_news() methods
        """
        urls = set()
        domains = set()
        api_sources = []
        
        # Add API sources
        api_sources.append("NewsAPI (newsapi.org)")
        
        # Add Google search if used
        if use_google:
            api_sources.append("Google Custom Search API")
        
        # Add Indian news sources that are always potentially used
        indian_sources = [
            "moneycontrol.com",
            "economictimes.indiatimes.com",
            "livemint.com",
            "business-standard.com",
            "financialexpress.com",
            "cnbctv18.com"
        ]
        domains.update(indian_sources)
        
        # Dynamically collect URLs and domains from ALL news categories in results
        # This works for any key ending with 'news' or 'results'
        news_categories = [key for key in results.keys()
                          if key.endswith(('news', 'results')) and isinstance(results[key], list)]
        
        for category in news_categories:
            if results[category]:  # Only process if category has data
                for item in results[category]:
                    url = item.get('url')
                    if url and url != 'N/A' and url.startswith(('http://', 'https://')):
                        urls.add(url)
                        domain = self._extract_domain(url)
                        if domain and domain != "Unknown":
                            domains.add(domain)
        
        return {
            'urls': sorted(list(urls)),
            'domains': sorted(list(domains)),
            'api_sources': api_sources
        }

# Convenience functions for easy usage
def search_stock_news(query: str, use_google: bool = False) -> Dict[str, Any]:
    """
    Stock-specific search for news and information
    
    Args:
        query: Search query (company name like "TCS", "Reliance")
        use_google: Whether to include Google search results (optional, default False)
        
    Returns:
        Dictionary with stock-specific analysis including:
        - Specific stock news from Indian sources
        - Optional Google search results
        - Batch summaries for each source type
        - Overall summary combining all sources
        - All source links used
    """
    agent = SearchAgent()
    return agent.execute(query, use_google=use_google)

def search_generic_news(query: str, use_google: bool = False) -> Dict[str, Any]:
    """
    Generic market search for broader queries
    
    Args:
        query: Market query (e.g., "top 10 Indian stocks", "market trends", "IPO news")
        use_google: Whether to include Google search results (optional, default False)
        
    Returns:
        Dictionary with market analysis including:
        - News results from multiple sources
        - Optional Google search results
        - Batch summaries for each source type
        - Overall summary combining all sources
        - All source links used
    """
    agent = SearchAgent()
    return agent.search_generic_news(query, use_google=use_google)

# Example usage
if __name__ == "__main__":
    # 1. Stock search with Google (comprehensive)
    print("=== Stock Search (With Google) ===")
    stock_results = search_stock_news("Reliance", use_google=True)
    print(f"Query: {stock_results['query']}")
    print(f"News Org Summary: {stock_results['news_org_summary']}")
    print(f"Google Summary: {stock_results['google_summary']}")
    print(f"Overall Summary: {stock_results['overall_summary']}")
    print(f"Domains: {', '.join(stock_results['sources']['domains'])}")
    
    # 2. Generic market search with Google
    print("\n=== Generic Market Search (With Google) ===")
    market_results = search_generic_news("banking sector analysis", use_google=True)
    print(f"Query: {market_results['query']}")
    print(f"News Org Summary: {market_results['news_org_summary']}")
    print(f"Google Summary: {market_results['google_summary']}")
    print(f"Overall Summary: {market_results['overall_summary']}")
    print(f"Domains: {', '.join(market_results['sources']['domains'])}")