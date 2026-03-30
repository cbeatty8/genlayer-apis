"""
Weather API helpers using Open-Meteo (no API key required).

Open-Meteo provides free weather data for non-commercial use.
https://open-meteo.com/
"""

import json
import genlayer.gl as gl


def get_weather(city: str, country_code: str = "") -> dict:
    """
    Get current weather for a city.

    Uses Open-Meteo geocoding + forecast API. No API key required.

    :param city: City name (e.g. "Jakarta", "Tokyo", "London")
    :param country_code: Optional ISO 3166-1 alpha-2 country code (e.g. "ID", "JP")
    :returns: dict with keys: city, country, temperature_c, windspeed_kmh, weathercode

    Example::

        weather = get_weather("Jakarta")
        # {'city': 'Jakarta', 'country': 'Indonesia', 'temperature_c': 28.5, ...}
    """
    # Step 1: Geocode city name to lat/lon
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    if country_code:
        geo_url += f"&country_code={country_code}"

    geo_response = gl.get_from_web(url=geo_url, mode="raw")
    geo_data = json.loads(geo_response)

    if not geo_data.get("results"):
        raise ValueError(f"City not found: {city}")

    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]

    # Step 2: Get current weather
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )

    weather_response = gl.get_from_web(url=weather_url, mode="raw")
    weather_data = json.loads(weather_response)

    current = weather_data["current_weather"]

    return {
        "city": location.get("name", city),
        "country": location.get("country", ""),
        "latitude": lat,
        "longitude": lon,
        "temperature_c": current["temperature"],
        "windspeed_kmh": current["windspeed"],
        "weathercode": current["weathercode"],
        "time": current["time"],
    }


def get_weather_forecast(city: str, days: int = 3, country_code: str = "") -> list[dict]:
    """
    Get daily weather forecast for a city.

    :param city: City name
    :param days: Number of forecast days (1-16)
    :param country_code: Optional country code
    :returns: list of dicts, each with keys: date, temp_max_c, temp_min_c, precipitation_mm, weathercode

    Example::

        forecast = get_weather_forecast("Tokyo", days=5)
        # [{'date': '2026-03-30', 'temp_max_c': 18.2, ...}, ...]
    """
    if days < 1 or days > 16:
        raise ValueError("days must be between 1 and 16")

    # Geocode
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    if country_code:
        geo_url += f"&country_code={country_code}"

    geo_response = gl.get_from_web(url=geo_url, mode="raw")
    geo_data = json.loads(geo_response)

    if not geo_data.get("results"):
        raise ValueError(f"City not found: {city}")

    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]

    # Forecast
    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode"
        f"&forecast_days={days}"
    )

    forecast_response = gl.get_from_web(url=forecast_url, mode="raw")
    forecast_data = json.loads(forecast_response)

    daily = forecast_data["daily"]
    result = []
    for i in range(len(daily["time"])):
        result.append({
            "date": daily["time"][i],
            "temp_max_c": daily["temperature_2m_max"][i],
            "temp_min_c": daily["temperature_2m_min"][i],
            "precipitation_mm": daily["precipitation_sum"][i],
            "weathercode": daily["weathercode"][i],
        })

    return result
