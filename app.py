# app.py
from services.aircraft_service import fetch_aircraft
from services.weather_service import fetch_weather
from services.alert_service import fetch_alerts

def main():
    print("Starting dashboard data fetch...")
    
    # Even if one API fails, the others will still run and the program won't crash
    aircraft_data = fetch_aircraft()
    weather_data = fetch_weather()
    alert_data = fetch_alerts()
    
    print("Data fetch cycle complete!")

if __name__ == "__main__":
    main()
