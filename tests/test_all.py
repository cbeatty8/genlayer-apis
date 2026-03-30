# tests for genlayer-apis
# These tests mock gl.get_from_web() since we can't make real HTTP calls in unit tests

import json
import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock genlayer.gl module before importing our modules
mock_gl = MagicMock()
sys.modules['genlayer'] = MagicMock()
sys.modules['genlayer.gl'] = mock_gl
sys.modules['genlayer.gl'] = mock_gl

from genlayer_apis import weather, crypto, web


class TestWeather(unittest.TestCase):

    @patch('genlayer_apis.weather.gl')
    def test_get_weather_success(self, mock_gl):
        mock_gl.get_from_web.side_effect = [
            json.dumps({"results": [{"name": "Jakarta", "country": "Indonesia", "latitude": -6.2, "longitude": 106.85}]}),
            json.dumps({"current_weather": {"temperature": 28.5, "windspeed": 12.0, "weathercode": 1, "time": "2026-03-30T09:00"}}),
        ]
        result = weather.get_weather("Jakarta")
        self.assertEqual(result["city"], "Jakarta")
        self.assertEqual(result["temperature_c"], 28.5)
        self.assertIn("latitude", result)
        self.assertIn("longitude", result)

    @patch('genlayer_apis.weather.gl')
    def test_get_weather_city_not_found(self, mock_gl):
        mock_gl.get_from_web.return_value = json.dumps({"results": []})
        with self.assertRaises(ValueError):
            weather.get_weather("NonexistentCity12345")

    @patch('genlayer_apis.weather.gl')
    def test_get_weather_forecast(self, mock_gl):
        mock_gl.get_from_web.side_effect = [
            json.dumps({"results": [{"name": "Tokyo", "country": "Japan", "latitude": 35.68, "longitude": 139.69}]}),
            json.dumps({"daily": {
                "time": ["2026-03-30", "2026-03-31"],
                "temperature_2m_max": [18.2, 19.5],
                "temperature_2m_min": [10.1, 11.3],
                "precipitation_sum": [0.0, 2.5],
                "weathercode": [1, 61],
            }}),
        ]
        result = weather.get_weather_forecast("Tokyo", days=2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["date"], "2026-03-30")
        self.assertEqual(result[1]["temp_max_c"], 19.5)

    def test_get_weather_forecast_invalid_days(self):
        with self.assertRaises(ValueError):
            weather.get_weather_forecast("Tokyo", days=0)
        with self.assertRaises(ValueError):
            weather.get_weather_forecast("Tokyo", days=20)


class TestCrypto(unittest.TestCase):

    @patch('genlayer_apis.crypto.gl')
    def test_get_price(self, mock_gl):
        mock_gl.get_from_web.return_value = json.dumps({
            "bitcoin": {
                "usd": 87500.0,
                "usd_market_cap": 1730000000000,
                "usd_24h_vol": 25000000000,
                "usd_24h_change": 2.5,
            }
        })
        result = crypto.get_price("BTC")
        self.assertEqual(result["symbol"], "BTC")
        self.assertEqual(result["price"], 87500.0)
        self.assertEqual(result["change_24h_pct"], 2.5)

    @patch('genlayer_apis.crypto.gl')
    def test_get_prices(self, mock_gl):
        mock_gl.get_from_web.return_value = json.dumps({
            "bitcoin": {"usd": 87500.0, "usd_market_cap": 1730000000000, "usd_24h_vol": 25000000000, "usd_24h_change": 2.5},
            "ethereum": {"usd": 3200.0, "usd_market_cap": 385000000000, "usd_24h_vol": 12000000000, "usd_24h_change": -1.2},
        })
        result = crypto.get_prices(["BTC", "ETH"])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["symbol"], "BTC")
        self.assertEqual(result[1]["symbol"], "ETH")

    @patch('genlayer_apis.crypto.gl')
    def test_get_market_data(self, mock_gl):
        mock_gl.get_from_web.return_value = json.dumps({
            "name": "Ethereum",
            "market_data": {
                "current_price": {"usd": 3200.0},
                "market_cap": {"usd": 385000000000},
                "total_volume": {"usd": 12000000000},
                "price_change_percentage_24h": -1.2,
                "price_change_percentage_7d": 5.3,
                "ath": {"usd": 4878.26},
                "ath_date": {"usd": "2021-11-10T14:24:11.849Z"},
                "circulating_supply": 120000000,
                "total_supply": 0,
            }
        })
        result = crypto.get_market_data("ETH")
        self.assertEqual(result["name"], "Ethereum")
        self.assertEqual(result["price"], 3200.0)
        self.assertEqual(result["change_7d_pct"], 5.3)

    def test_coin_id_resolution(self):
        self.assertEqual(crypto._resolve_coin_id("BTC"), "bitcoin")
        self.assertEqual(crypto._resolve_coin_id("eth"), "ethereum")
        self.assertEqual(crypto._resolve_coin_id("my-coin"), "my-coin")


class TestWeb(unittest.TestCase):

    @patch('genlayer_apis.web.gl')
    def test_fetch_json(self, mock_gl):
        mock_gl.get_from_web.return_value = json.dumps({"key": "value"})
        result = web.fetch_json("https://example.com/api")
        self.assertEqual(result, {"key": "value"})

    @patch('genlayer_apis.web.gl')
    def test_fetch_text(self, mock_gl):
        mock_gl.get_from_web.return_value = "<html><body>Hello</body></html>"
        result = web.fetch_text("https://example.com")
        self.assertEqual(result, "<html><body>Hello</body></html>")

    @patch('genlayer_apis.web.gl')
    def test_scrape_links(self, mock_gl):
        mock_gl.get_from_web.return_value = '<a href="https://github.com/test">link1</a><a href="https://other.com">link2</a>'
        result = web.scrape_links("https://example.com", filter_pattern="github.com")
        self.assertEqual(result, ["https://github.com/test"])

    @patch('genlayer_apis.web.gl')
    def test_scrape_text(self, mock_gl):
        mock_gl.get_from_web.return_value = "<body><p>Hello World</p><p>Second paragraph</p></body>"
        result = web.scrape_text("https://example.com", tag="p")
        self.assertIn("Hello World", result)
        self.assertIn("Second paragraph", result)


if __name__ == "__main__":
    unittest.main()
