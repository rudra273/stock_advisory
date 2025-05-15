import requests
from app.core.config import settings

api_key = settings.GOOGLE_SEARCH_API_KEY
search_engine_id = settings.SEARCH_ENGINE_ID
query = "machine learning"
url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
response = requests.get(url)
results = response.json()
for item in results.get("items", []):
    print(item["title"], item["link"])

# new line