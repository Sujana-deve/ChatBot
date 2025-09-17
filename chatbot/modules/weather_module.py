# chatbot/modules/weather_module.py
import requests

# Directly use your API key
API_KEY = "e39ecaa7bf1f981229b8762e148ad039"

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def geocode_place(place: str):
    """Get latitude/longitude from place name."""
    params = {"q": place, "limit": 1, "appid": API_KEY}
    r = requests.get(GEOCODE_URL, params=params, timeout=10)
    data = r.json()
    if not data:
        return None
    return {
        "name": data[0].get("name"),
        "lat": data[0]["lat"],
        "lon": data[0]["lon"],
        "country": data[0].get("country"),
    }

def get_weather_by_place(place: str):
    """Fetch weather details for a given place."""
    geo = geocode_place(place)
    if not geo:
        return None, f"Could not find location '{place}'. Please provide a city and country if ambiguous."

    params = {"lat": geo["lat"], "lon": geo["lon"], "appid": API_KEY, "units": "metric"}
    r = requests.get(WEATHER_URL, params=params, timeout=10)
    
    if r.status_code != 200:
        return None, "Weather API error."

    w = r.json()
    summary = w["weather"][0]["description"].capitalize()
    temp = w["main"]["temp"]
    feels = w["main"].get("feels_like")
    humidity = w["main"].get("humidity")

    return geo, (
        f"Weather in {geo['name']}, {geo.get('country','')}: "
        f"{summary}, {temp}°C (feels like {feels}°C). Humidity: {humidity}%."
    )
