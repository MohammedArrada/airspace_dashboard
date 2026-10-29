import json
from services.aircraft_service import fetch_aircraft
from services.weather_service import fetch_weather
from services.alert_service import fetch_alerts


for name, func in [("aircraft", fetch_aircraft), ("weather", fetch_weather), ("alerts", fetch_alerts)]:
    data = func()
    if data is None:
        print(f"{name}: FAILED")
        continue
    print(f"{name}: OK, top-level type = {type(data).__name__}")
    with open(f"cache/sample_{name}.json", "w") as f:
        json.dump(data, f, indent=2)