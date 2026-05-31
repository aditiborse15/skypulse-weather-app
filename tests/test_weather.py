# ============================================================
#  tests/test_weather.py
#  Run with: pytest tests/
# ============================================================

import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from weather_cli import kelvin_to_celsius, get_wind_direction, get_weather_emoji, get_current_weather


# ── Unit tests (no API calls needed) ─────────────────────

class TestHelperFunctions:

    def test_kelvin_to_celsius_boiling(self):
        assert kelvin_to_celsius(373.15) == 100.0

    def test_kelvin_to_celsius_freezing(self):
        assert kelvin_to_celsius(273.15) == 0.0

    def test_kelvin_to_celsius_body_temp(self):
        assert kelvin_to_celsius(310.15) == 37.0

    def test_wind_direction_north(self):
        assert get_wind_direction(0) == "N"

    def test_wind_direction_east(self):
        assert get_wind_direction(90) == "E"

    def test_wind_direction_south(self):
        assert get_wind_direction(180) == "S"

    def test_wind_direction_west(self):
        assert get_wind_direction(270) == "W"

    def test_emoji_clear(self):
        assert get_weather_emoji("Clear") == "☀️"

    def test_emoji_rain(self):
        assert get_weather_emoji("Rain") == "🌧️"

    def test_emoji_snow(self):
        assert get_weather_emoji("Snow") == "❄️"

    def test_emoji_unknown(self):
        assert get_weather_emoji("Tornado") == "🌡️"


# ── Integration tests (mock the API so no real calls) ────

class TestGetCurrentWeather:

    # This is a fake API response that looks like the real one
    FAKE_RESPONSE = {
        "name": "Mumbai",
        "sys": {"country": "IN"},
        "main": {
            "temp": 31.5, "feels_like": 34.0,
            "temp_min": 28.0, "temp_max": 35.0,
            "humidity": 72, "pressure": 1008
        },
        "wind": {"speed": 4.2, "deg": 200},
        "visibility": 8000,
        "clouds": {"all": 40},
        "weather": [{"main": "Clouds", "description": "scattered clouds"}]
    }

    @patch("weather_cli.requests.get")
    def test_successful_fetch(self, mock_get):
        """Test that valid city returns correct data."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = self.FAKE_RESPONSE
        mock_get.return_value = mock_resp

        result = get_current_weather("Mumbai")

        assert result is not None
        assert result["name"] == "Mumbai"
        assert result["main"]["temp"] == 31.5

    @patch("weather_cli.requests.get")
    def test_city_not_found(self, mock_get):
        """Test that 404 returns None."""
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp

        result = get_current_weather("FakeCityXYZ")
        assert result is None

    @patch("weather_cli.requests.get")
    def test_invalid_api_key(self, mock_get):
        """Test that 401 (bad API key) returns None."""
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_get.return_value = mock_resp

        result = get_current_weather("Mumbai")
        assert result is None
