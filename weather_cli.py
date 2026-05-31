# ============================================================
#  SkyPulse - Weather App (CLI Version)
#  Built with: Python + OpenWeatherMap API
#  Author: Your Name
# ============================================================

import requests   # to call the weather API
import os         # to read the API key from .env file
from dotenv import load_dotenv  # pip install python-dotenv

# Load the API key from .env file (keeps it secret)
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")

# Base URL for OpenWeatherMap API
BASE_URL = "https://api.openweathermap.org/data/2.5"


# ── Helper Functions ──────────────────────────────────────

def kelvin_to_celsius(kelvin):
    """Convert temperature from Kelvin to Celsius."""
    return round(kelvin - 273.15, 1)


def get_wind_direction(degrees):
    """Convert wind degree to compass direction (N, NE, E, etc.)"""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return directions[index]


def get_weather_emoji(condition):
    """Return an emoji based on weather condition."""
    condition = condition.lower()
    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "thunder" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    else:
        return "🌡️"


# ── API Call Functions ────────────────────────────────────

def get_current_weather(city):
    """
    Fetch current weather for a city.
    Returns a dictionary with weather data, or None if error.
    """
    url = f"{BASE_URL}/weather"

    # Parameters we send to the API
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # metric = Celsius, imperial = Fahrenheit
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        # 200 means success, 404 means city not found, 401 means bad API key
        if response.status_code == 404:
            print(f"❌ City '{city}' not found. Please check the spelling.")
            return None
        elif response.status_code == 401:
            print("❌ Invalid API key. Check your .env file.")
            return None
        elif response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            return None

        # Convert the JSON response to a Python dictionary
        data = response.json()
        return data

    except requests.exceptions.ConnectionError:
        print("❌ No internet connection. Please check your network.")
        return None
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again.")
        return None


def get_forecast(city):
    """
    Fetch 5-day weather forecast (every 3 hours = 40 data points).
    Returns list of forecast items, or None if error.
    """
    url = f"{BASE_URL}/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()
        return data["list"]  # list of 40 forecast entries

    except requests.exceptions.RequestException:
        return None


# ── Display Functions ─────────────────────────────────────

def display_current_weather(data):
    """Print current weather in a nice format."""

    city        = data["name"]
    country     = data["sys"]["country"]
    temp        = data["main"]["temp"]
    feels_like  = data["main"]["feels_like"]
    temp_min    = data["main"]["temp_min"]
    temp_max    = data["main"]["temp_max"]
    humidity    = data["main"]["humidity"]
    pressure    = data["main"]["pressure"]
    wind_speed  = data["wind"]["speed"]
    wind_deg    = data["wind"].get("deg", 0)
    visibility  = data.get("visibility", 0) / 1000   # convert m → km
    clouds      = data["clouds"]["all"]
    description = data["weather"][0]["description"].capitalize()
    condition   = data["weather"][0]["main"]
    emoji       = get_weather_emoji(condition)

    print("\n" + "=" * 45)
    print(f"  {emoji}  Weather in {city}, {country}")
    print("=" * 45)
    print(f"  Temperature  : {temp}°C  (feels like {feels_like}°C)")
    print(f"  High / Low   : {temp_max}°C / {temp_min}°C")
    print(f"  Condition    : {description}")
    print(f"  Humidity     : {humidity}%")
    print(f"  Wind         : {wind_speed} m/s {get_wind_direction(wind_deg)}")
    print(f"  Pressure     : {pressure} hPa")
    print(f"  Visibility   : {visibility:.1f} km")
    print(f"  Cloud Cover  : {clouds}%")
    print("=" * 45)


def display_forecast(forecast_list):
    """Print a simplified 5-day forecast (one entry per day at noon)."""

    print("\n  📅  5-Day Forecast")
    print("-" * 45)

    seen_days = set()   # track which days we've already shown

    for item in forecast_list:
        # item["dt_txt"] looks like "2024-05-31 12:00:00"
        date_str = item["dt_txt"]
        date_part = date_str.split(" ")[0]   # "2024-05-31"
        time_part = date_str.split(" ")[1]   # "12:00:00"

        # Only show the noon reading for each day
        if "12:00:00" in time_part and date_part not in seen_days:
            seen_days.add(date_part)

            temp        = item["main"]["temp"]
            temp_min    = item["main"]["temp_min"]
            temp_max    = item["main"]["temp_max"]
            description = item["weather"][0]["description"].capitalize()
            condition   = item["weather"][0]["main"]
            emoji       = get_weather_emoji(condition)

            print(f"  {date_part}  {emoji}  {temp}°C  ({temp_min}°–{temp_max}°)  {description}")

    print("-" * 45)


# ── Main Program ──────────────────────────────────────────

def main():
    print("\n🌤️  Welcome to SkyPulse Weather App")
    print("   Powered by OpenWeatherMap API\n")

    while True:
        # Ask user for a city
        city = input("Enter city name (or 'quit' to exit): ").strip()

        if city.lower() in ("quit", "exit", "q"):
            print("\n👋 Goodbye!\n")
            break

        if not city:
            print("⚠️  Please enter a city name.\n")
            continue

        # 1. Get and show current weather
        print(f"\n⟳ Fetching weather for '{city}'...")
        weather_data = get_current_weather(city)

        if weather_data:
            display_current_weather(weather_data)

            # 2. Ask if user wants forecast
            choice = input("\n  Show 5-day forecast? (y/n): ").strip().lower()
            if choice == "y":
                forecast_data = get_forecast(city)
                if forecast_data:
                    display_forecast(forecast_data)

        print()  # blank line before next search


# Run the program
if __name__ == "__main__":
    main()
