def normalize_aircraft(raw_data):

    if not raw_data:
        return []

    states = raw_data.get("states") or []
    aircraft = []

    for state in states:
        if len(state) < 10:
            continue 

        callsign = state[1].strip() if state[1] else None

        aircraft.append({
            "icao24": state[0],
            "callsign": callsign,
            "country": state[2],
            "longitude": state[5],
            "latitude": state[6],
            "altitude_meters": state[7],
            "velocity_mps": state[9],
            "on_ground": state[8],
        })

    return aircraft


def normalize_weather(raw_data):

    if not raw_data:
        return []

    observations = []
    for item in raw_data:
        observations.append({
            "airport": item.get("icaoId"),
            "observed_at": item.get("obsTime"),
            "temperature_c": item.get("temp"),
            "wind_direction": item.get("wdir"),
            "wind_speed_kt": item.get("wspd"),
            "visibility": item.get("visib"),
            "flight_category": item.get("fltCat"),
            "raw_metar": item.get("rawOb"),
        })

    return observations



#part 5: processing functions
def count_airborne_aircraft(aircraft):
    return sum(1 for a in aircraft if a["on_ground"] is False)


def count_ground_aircraft(aircraft):
    return sum(1 for a in aircraft if a["on_ground"] is True)


def find_fastest_aircraft(aircraft):
    with_speed = [a for a in aircraft if a["velocity_mps"] is not None]
    if not with_speed:
        return None
    return max(with_speed, key=lambda a: a["velocity_mps"])


def find_highest_aircraft(aircraft):
    with_altitude = [a for a in aircraft if a["altitude_meters"] is not None]
    if not with_altitude:
        return None
    return max(with_altitude, key=lambda a: a["altitude_meters"])


def find_aircraft_missing_positions(aircraft):
    return [
        a for a in aircraft
        if a["latitude"] is None or a["longitude"] is None
    ]


'''
VFR	Visual Flight Rules	--- Clear weather
MVFR	Marginal VFR  ----	Fair weather
IFR	Instrument Flight Rules	--- Poor weather
LIFR	Low IFR	--- Very bad weather

'''

def classify_weather_risk(weather):

    results = []
    for obs in weather:
        category = obs.get("flight_category")
        if category == "VFR":
            risk = "low"
        elif category == "MVFR":
            risk = "moderate"
        elif category in ("IFR", "LIFR"):
            risk = "high"
        else:
            risk = "unknown"
        results.append({"airport": obs.get("airport"), "risk": risk})
    return results



# filtering functions 
# /aircraft?status=airborne
# /aircraft?status=ground
# /aircraft?status=missing
# /aircraft?sort=altitude
# /aircraft?sort=speed
# /aircraft?search=TEST
def filter_aircraft(aircraft, status="all", sort="" ,search=""):
    result = list(aircraft)  

    #alphabetical sort by icao24
    result.sort(key=lambda a: a["icao24"] or "")  

    if status == "airborne":
        result = [a for a in result if a["on_ground"] is False]
    elif status == "ground":
        result = [a for a in result if a["on_ground"] is True]
    elif status == "missing":
        result = [a for a in result if has_missing_information(a)]

    if sort == "altitude":
        result = sort_aircraft(result, "altitude_meters")
    elif sort == "speed":
        result = sort_aircraft(result, "velocity_mps")

    search = search.strip().lower()
    if search:
        result = [
            a for a in result
            if search in (a["callsign"] or "").lower() or search in (a["icao24"] or "").lower() #to handle none values
        ]
    return result


def has_missing_information(a):
    fields = ["callsign", "longitude", "latitude", "altitude_meters", "velocity_mps"]
    return any(a[field] is None for field in fields)

def sort_aircraft(aircraft, key):
    with_value = [a for a in aircraft if a[key] is not None]
    without_value = [a for a in aircraft if a[key] is None]
    with_value.sort(key=lambda a: a[key], reverse=True)
    return with_value + without_value