import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from time import perf_counter

from flask import Flask, redirect, render_template, url_for

from services.aircraft_service import fetch_aircraft
from services.weather_service import fetch_weather
from services.alert_service import fetch_alerts
from services.data_processing import (
    normalize_aircraft, normalize_weather,
    count_airborne_aircraft, count_ground_aircraft,
    find_fastest_aircraft, find_highest_aircraft,
    find_aircraft_missing_positions, classify_weather_risk,
)

app = Flask(__name__)

DATA = {}


def load_sample(name):
    try:
        with open(f"cache/sample_{name}.json") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def refresh_data():
    start = perf_counter()
    with ThreadPoolExecutor(max_workers=3) as executor:
        aircraft_future = executor.submit(fetch_aircraft)
        weather_future = executor.submit(fetch_weather)
        alerts_future = executor.submit(fetch_alerts)
        raw_aircraft = aircraft_future.result()
        raw_weather = weather_future.result()
        raw_alerts = alerts_future.result()
    retrieval_time = perf_counter() - start

    ''' source_health 
    {
    "name": "Aviation Weather Center",
    "available": True,
    "using_cache": False,
    "message": "Current data received",
    "last_updated": "2026-10-26 10:15:00"
    }'''
    sources = {}
    # if raw_aircraft is not None:
    #     sources["OpenSky (aircraft)"] = "Live"
    # else:
    #     raw_aircraft = load_sample("aircraft")
    #     sources["OpenSky (aircraft)"] = "Saved sample" if raw_aircraft else "Failed"

    # if raw_weather is not None:
    #     sources["Aviation Weather (METAR)"] = "Live"
    # else:
    #     raw_weather = load_sample("weather")
    #     sources["Aviation Weather (METAR)"] = "Saved sample" if raw_weather else "Failed"

    # sources["NWS (alerts)"] = "Live" if raw_alerts is not None else "Failed"

    aircraft = normalize_aircraft(raw_aircraft)
    weather = normalize_weather(raw_weather)

    risks = {r["airport"]: r["risk"] for r in classify_weather_risk(weather)}
    for obs in weather:
        obs["risk"] = risks.get(obs["airport"])
        if obs["observed_at"] is not None:
            when = datetime.fromtimestamp(obs["observed_at"], tz=timezone.utc)
            obs["observed_text"] = when.strftime("%H:%M UTC")
        else:
            obs["observed_text"] = None

    summary = {
        "total": len(aircraft),
        "airborne": count_airborne_aircraft(aircraft),
        "ground": count_ground_aircraft(aircraft),
        "missing_positions": len(find_aircraft_missing_positions(aircraft)),
        "fastest": find_fastest_aircraft(aircraft),
        "highest": find_highest_aircraft(aircraft),
    }

    alert_events = []
    if raw_alerts:
        for feature in raw_alerts.get("features", []):
            alert_events.append(feature["properties"].get("event"))

    DATA.update({
        "aircraft": aircraft,
        "weather": weather,
        "summary": summary,
        "sources": sources,
        "alert_events": alert_events,
        "retrieval_time": round(retrieval_time, 2),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


def ensure_data():
    if not DATA:
        refresh_data()


@app.route("/")
def dashboard():
    ensure_data()
    return render_template("dashboard.html", **DATA)

@app.route("/aircraft")
def aircraft_page():
    ensure_data()
    return render_template("aircraft.html", **DATA)

@app.route("/weather")
def weather_page():
    ensure_data()
    return render_template("weather.html", **DATA)

@app.route("/refresh")
def refresh():
    refresh_data()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True,port=5001)