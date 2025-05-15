import requests
from bs4 import BeautifulSoup
import json
import re

def get_cnn_fear_greed_index():
    """
    Fetches the current CNN Fear & Greed Index.

    Returns:
        dict: A dictionary containing the Fear & Greed Index data,
              or None if an error occurs.
              The dictionary typically includes:
              - 'fear_and_greed': {
                  'score': float, current index value
                  'rating': string, e.g., "Fear", "Neutral", "Greed"
                  'timestamp': string, last update time
                }
              - 'fear_and_greed_historical': { ... historical data ... }
              - 'market_momentum_sp500': { ... data for this indicator ... }
              - etc. for all 7 indicators.
    """
    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CNN Fear & Greed Index: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response from CNN Fear & Greed Index.")
        return None


def get_market_mood_index():
    """
    Scrapes the Market Mood Index (MMI) from the Tickertape website.
    
    Returns:
        dict: A dictionary containing:
            - 'mmi_value': The current MMI value as a float
            - 'mmi_zone': The current market mood zone (e.g., 'Extreme Greed')
            - 'last_updated': When the MMI was last updated
    
    Raises:
        ConnectionError: If unable to connect to the website
        ValueError: If unable to parse the MMI value from the page
    """
    url = "https://www.tickertape.in/market-mood-index"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the MMI value
        mmi_value_element = soup.select_one("div.mmi-value span.number")
        if not mmi_value_element:
            raise ValueError("Could not find MMI value element on the page")
        
        mmi_value = float(mmi_value_element.text.strip())
        
        # Find the last updated information
        last_updated_element = soup.select_one("div.mmi-value p.date")
        last_updated = last_updated_element.text.strip() if last_updated_element else "Unknown"
        
        # Determine the current mood zone
        # We can extract this from the page or determine it based on the MMI value
        if mmi_value > 70:
            mood_zone = "Extreme Greed"
        elif mmi_value > 50:
            mood_zone = "Greed"
        elif mmi_value > 30:
            mood_zone = "Fear"
        else:
            mood_zone = "Extreme Fear"
        
        # For more accurate zone determination, we can also extract it directly from the page
        mood_text = soup.select_one("p.text.text-secondary")
        if mood_text:
            zone_match = re.search(r'MMI is in <span class="font-medium">the (.*?) zone', mood_text.text)
            if zone_match:
                mood_zone = zone_match.group(1).strip().title()
        
        return {
            "mmi_value": mmi_value,
            "mmi_zone": mood_zone,
            "last_updated": last_updated
        }
        
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to Tickertape: {e}")
    except ValueError as e:
        raise ValueError(f"Error parsing MMI data: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")


def fear_greed_index():
    try:
        cnn_index_data = get_cnn_fear_greed_index()
        if not cnn_index_data:
            return None
            
        score = int(round(cnn_index_data['fear_and_greed']['score']))
        rating = cnn_index_data['fear_and_greed']['rating']
        timestamp = cnn_index_data['fear_and_greed']['timestamp']
        
        return {
            'score': score,
            'rating': rating,
            'last_updated': timestamp,
            'source': 'CNN Fear & Greed Index'
        }
    except Exception as e:
        print(f"Error formatting CNN Fear & Greed Index: {e}")
        return None

def mmi():
    try:
        mmi_data = get_market_mood_index()
        return {
            'score': int(round(mmi_data['mmi_value'])),
            'rating': mmi_data['mmi_zone'],
            'last_updated': mmi_data['last_updated'],
            'source': 'Tickertape Market Mood Index'
        }
    except Exception as e:
        print(f"Error fetching Market Mood Index: {e}")
        return None

# if __name__ == '__main__':
#     # Get CNN Fear & Greed Index
#     cnn_data = fear_greed_index()
#     if cnn_data:
#         print("--- CNN Fear & Greed Index ---")
#         print(f"Score: {cnn_data['score']}")
#         print(f"Rating: {cnn_data['rating']}")
#         print(f"Last Updated: {cnn_data['last_updated']}")
#         print(f"Source: {cnn_data['source']}")
#     else:
#         print("Failed to retrieve CNN Fear & Greed Index.")
    
#     # Get Market Mood Index
#     mmi_data = mmi()
#     if mmi_data:
#         print("\n--- Market Mood Index ---")
#         print(f"Score: {mmi_data['score']}")
#         print(f"Rating: {mmi_data['rating']}")
#         print(f"Last Updated: {mmi_data['last_updated']}")
#         print(f"Source: {mmi_data['source']}")
#     else:
#         print("\nFailed to retrieve Market Mood Index.")