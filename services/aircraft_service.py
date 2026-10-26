import requests

URL = "https://opensky-network.org/api/states/all?lamin=38.3&lomin=-77.8&lamax=39.5&lomax=-76.3"

def fetch_aircraft():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Aircraft fetch failed: {e}")
        return None