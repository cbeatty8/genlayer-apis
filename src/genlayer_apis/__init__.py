"""
genlayer-apis: Standardized API helpers for GenLayer Intelligent Contracts

Provides easy-to-use functions for contracts to interact with external APIs:
- Weather data (Open-Meteo)
- Crypto prices (CoinGecko)
- JSON fetching (generic)
- HTML scraping (basic)

All functions use gl.get_from_web() internally and return parsed data.
"""

__version__ = "0.1.0"

from .weather import get_weather, get_weather_forecast
from .crypto import get_price, get_prices, get_market_data
from .web import fetch_json, fetch_text, scrape_links, scrape_text

__all__ = [
    "get_weather",
    "get_weather_forecast",
    "get_price",
    "get_prices",
    "get_market_data",
    "fetch_json",
    "fetch_text",
    "scrape_links",
    "scrape_text",
]
