import requests

URL = "https://api.weather.gov/alerts/active?area=MD"
HEADERS = {"User-Agent": "StructuredProgrammingCourse-AirspaceDashboard"}

def fetch_alerts():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Alerts fetch failed: {e}")
        return None