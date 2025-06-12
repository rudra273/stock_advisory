# app/services/crawler/scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, timeout: int = 10, delay: float = 1.0):
        """
        Initialize the web scraper.
        
        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests in seconds
        """
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common unwanted patterns
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\t+', ' ', text)
        
        return text

    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main text content from BeautifulSoup object.
        
        Args:
            soup: BeautifulSoup parsed HTML
            
        Returns:
            Extracted text content
        """
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()

        # Try to find main content areas first
        main_content = None
        content_selectors = [
            'main',
            'article', 
            '.content',
            '.main-content',
            '.article-content',
            '.post-content',
            '#content',
            '#main'
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            main_content = soup
        
        # Extract text
        text = main_content.get_text()
        return self._clean_text(text)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract all links from the page.
        
        Args:
            soup: BeautifulSoup parsed HTML
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            # Filter out non-HTTP links and fragments
            if absolute_url.startswith(('http://', 'https://')) and '#' not in absolute_url:
                links.append(absolute_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links

    def scrape_url(self, url: str, max_words: Optional[int] = 1500) -> Dict:
        """
        Scrape a single URL and extract content and links.
        
        Args:
            url: URL to scrape
            max_words: Maximum number of words to return (None for no limit)
            
        Returns:
            Dictionary containing:
            - url: The scraped URL
            - title: Page title
            - content: Extracted text content
            - links: List of links found on the page
            - status: Success status
            - error: Error message if any
        """
        result = {
            'url': url,
            'title': '',
            'content': '',
            'links': [],
            'status': 'failed',
            'error': None
        }
        
        try:
            logger.info(f"Scraping URL: {url}")
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Check if content is HTML
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                result['error'] = f"Content type not supported: {content_type}"
                return result
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            result['title'] = self._clean_text(title_tag.get_text()) if title_tag else ''
            
            # Extract content
            content = self._extract_text_content(soup)
            
            # Limit words if specified
            if max_words and content:
                words = content.split()
                if len(words) > max_words:
                    content = ' '.join(words[:max_words]) + '...'
            
            result['content'] = content
            
            # Extract links
            result['links'] = self._extract_links(soup, url)
            
            result['status'] = 'success'
            logger.info(f"Successfully scraped: {url}")
            
        except requests.exceptions.RequestException as e:
            result['error'] = f"Request error: {str(e)}"
            logger.error(f"Request error for {url}: {e}")
            
        except Exception as e:
            result['error'] = f"Parsing error: {str(e)}"
            logger.error(f"Parsing error for {url}: {e}")
        
        return result

    def scrape_multiple_urls(self, urls: List[str], max_words: Optional[int] = 1500) -> List[Dict]:
        """
        Scrape multiple URLs with delay between requests.
        
        Args:
            urls: List of URLs to scrape
            max_words: Maximum number of words per page (None for no limit)
            
        Returns:
            List of dictionaries with scraping results
        """
        results = []
        
        for i, url in enumerate(urls):
            if i > 0:  # Add delay between requests
                time.sleep(self.delay)
            
            result = self.scrape_url(url, max_words)
            results.append(result)
        
        return results

    def get_successful_results(self, results: List[Dict]) -> List[Dict]:
        """
        Filter results to only return successful scrapes.
        
        Args:
            results: List of scraping results
            
        Returns:
            List of successful results only
        """
        return [result for result in results if result['status'] == 'success']


# Convenience functions
def scrape_single_page(url: str, max_words: int = 1500, timeout: int = 10) -> Dict:
    """
    Convenience function to scrape a single page.
    
    Args:
        url: URL to scrape
        max_words: Maximum number of words to return
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with scraping results
    """
    scraper = WebScraper(timeout=timeout)
    return scraper.scrape_url(url, max_words)


def scrape_multiple_pages(urls: List[str], max_words: int = 1500, timeout: int = 10, delay: float = 1.0) -> List[Dict]:
    """
    Convenience function to scrape multiple pages.
    
    Args:
        urls: List of URLs to scrape
        max_words: Maximum number of words per page
        timeout: Request timeout in seconds
        delay: Delay between requests in seconds
        
    Returns:
        List of dictionaries with scraping results
    """
    scraper = WebScraper(timeout=timeout, delay=delay)
    return scraper.scrape_multiple_urls(urls, max_words)


def scrape_google_results(google_results: List[Dict], max_words: int = 1500) -> List[Dict]:
    """
    Convenience function to scrape URLs from Google search results.
    
    Args:
        google_results: List of Google search results (each with 'link' key)
        max_words: Maximum number of words per page
        
    Returns:
        List of dictionaries with scraping results
    """
    urls = [result.get('link') for result in google_results if result.get('link')]
    urls = [url for url in urls if url]  # Remove None values
    
    return scrape_multiple_pages(urls, max_words)


# # Example usage functions for testing
# if __name__ == "__main__":
#     # Test single URL scraping
#     test_url = "https://example.com"
#     result = scrape_single_page(test_url)
#     print(f"Title: {result['title']}")
#     print(f"Content preview: {result['content'][:200]}...")
#     print(f"Found {len(result['links'])} links")
    
#     # Test multiple URLs
#     test_urls = ["https://example.com", "https://httpbin.org/html"]
#     results = scrape_multiple_pages(test_urls)
#     for result in results:
#         print(f"URL: {result['url']}")
#         print(f"Status: {result['status']}")
#         if result['status'] == 'success':
#             print(f"Title: {result['title']}")
#             print(f"Content length: {len(result['content'])} characters")
#         else:
#             print(f"Error: {result['error']}")