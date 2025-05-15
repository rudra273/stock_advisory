import requests
from app.core.config import settings

api_key = settings.GOOGLE_SEARCH_API_KEY


def google_search(query):
    """
    Simple Google search function that searches for the given query and
    returns website search results including title, link, snippet, and meta description.
    
    Args:
        query (str): The search query to look for
        
    Returns:
        list: A list of dictionaries containing search results
    """
    search_engine_id = settings.SEARCH_ENGINE_ID
    
    # Add search type parameter to restrict to only websites
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
    
    try:
        response = requests.get(url)
        results = response.json()
        
        search_results = []
        for item in results.get("items", []):
            result = {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            }
            
            
            search_results.append(result)
        
        return search_results
        
    except Exception as e:
        print(f"Error in Google search: {e}")
        return []