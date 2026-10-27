from services.aircraft_service import fetch_aircraft
from services.weather_service import fetch_weather
from services.data_processing import (
    normalize_aircraft, normalize_weather,
    count_airborne_aircraft, count_ground_aircraft,
    find_fastest_aircraft, find_highest_aircraft,
    find_aircraft_missing_positions, classify_weather_risk,
)

aircraft = normalize_aircraft(fetch_aircraft())
weather = normalize_weather(fetch_weather())

print("Normalized aircraft:", aircraft[0] if aircraft else None)
print("Normalized weather:", weather[0] if weather else None)


# print("Airborne:", count_airborne_aircraft(aircraft))
# print("On ground:", count_ground_aircraft(aircraft))
# print("Fastest:", find_fastest_aircraft(aircraft))
# print("Highest:", find_highest_aircraft(aircraft))
# print("Missing positions:", len(find_aircraft_missing_positions(aircraft)))
# print("Weather risk:", classify_weather_risk(weather))