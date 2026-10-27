from time import perf_counter
from concurrent.futures import ThreadPoolExecutor

from services.aircraft_service import fetch_aircraft
from services.weather_service import fetch_weather
from services.alert_service import fetch_alerts





# Sequential
start_time = perf_counter()
aircraft = fetch_aircraft()
weather = fetch_weather()
alerts = fetch_alerts()
end_time = perf_counter()
sequential_time = end_time - start_time
print(f"Sequential: {sequential_time:.3f} seconds")






# Concurrent
start_time = perf_counter()
with ThreadPoolExecutor(max_workers=3) as executor:
    aircraft_future = executor.submit(fetch_aircraft)
    weather_future = executor.submit(fetch_weather)
    alerts_future = executor.submit(fetch_alerts)

    aircraft = aircraft_future.result()
    weather = weather_future.result()
    alerts = alerts_future.result()
end_time = perf_counter()
concurrent_time = end_time - start_time
print(f"Concurrent: {concurrent_time:.3f} seconds")

print(f"Difference: {sequential_time - concurrent_time:.3f} seconds")