# ============================================================
#  SkyPulse - Weather App (Flask Web Version)
#  Run: python app.py  →  open http://127.0.0.1:5000
# ============================================================

from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY  = os.getenv("OWM_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

app = Flask(__name__)   # create the Flask app


# ── Helper (reused from CLI version) ─────────────────────

def get_weather_emoji(condition):
    condition = condition.lower()
    if "clear"   in condition: return "☀️"
    if "cloud"   in condition: return "☁️"
    if "rain"    in condition: return "🌧️"
    if "thunder" in condition: return "⛈️"
    if "snow"    in condition: return "❄️"
    if "mist"    in condition: return "🌫️"
    return "🌡️"


# ── Routes ────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/api/weather")
def weather():
    """
    API endpoint — returns JSON weather data.
    Usage: GET /api/weather?city=Mumbai
    """
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": "Please provide a city name."}), 400

    if not API_KEY:
        return jsonify({"error": "API key not configured."}), 500

    # ── Current weather ──
    resp = requests.get(
        f"{BASE_URL}/weather",
        params={"q": city, "appid": API_KEY, "units": "metric"},
        timeout=10
    )

    if resp.status_code == 404:
        return jsonify({"error": f"City '{city}' not found."}), 404
    if resp.status_code == 401:
        return jsonify({"error": "Invalid API key."}), 401
    if resp.status_code != 200:
        return jsonify({"error": "Weather API error."}), 502

    d = resp.json()

    # ── 5-day forecast ──
    forecast = []
    try:
        fr = requests.get(
            f"{BASE_URL}/forecast",
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10
        )
        if fr.status_code == 200:
            seen = set()
            for item in fr.json()["list"]:
                date = item["dt_txt"].split(" ")[0]
                time = item["dt_txt"].split(" ")[1]
                if "12:00:00" in time and date not in seen:
                    seen.add(date)
                    forecast.append({
                        "date":  date,
                        "temp":  item["main"]["temp"],
                        "min":   item["main"]["temp_min"],
                        "max":   item["main"]["temp_max"],
                        "desc":  item["weather"][0]["description"].capitalize(),
                        "emoji": get_weather_emoji(item["weather"][0]["main"]),
                    })
    except Exception:
        pass   # forecast is optional

    # Build the response dictionary
    result = {
        "city":        d["name"],
        "country":     d["sys"]["country"],
        "temp":        round(d["main"]["temp"], 1),
        "feels_like":  round(d["main"]["feels_like"], 1),
        "temp_min":    round(d["main"]["temp_min"], 1),
        "temp_max":    round(d["main"]["temp_max"], 1),
        "humidity":    d["main"]["humidity"],
        "pressure":    d["main"]["pressure"],
        "wind_speed":  d["wind"]["speed"],
        "visibility":  round(d.get("visibility", 0) / 1000, 1),
        "clouds":      d["clouds"]["all"],
        "description": d["weather"][0]["description"].capitalize(),
        "emoji":       get_weather_emoji(d["weather"][0]["main"]),
        "forecast":    forecast[:5],
    }

    return jsonify(result)


# ── Run the server ─────────────────────────────────────────

if __name__ == "__main__":
    # debug=True → auto-reloads when you change the code
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
