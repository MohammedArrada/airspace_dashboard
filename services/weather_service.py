import requests

URL = "https://aviationweather.gov/api/data/metar?ids=KDCA,KIAD,KBWI&format=json"

def fetch_weather():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Weather fetch failed: {e}")
        return None