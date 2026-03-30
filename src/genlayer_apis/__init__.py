"""
genlayer-apis: Standardized API helpers for GenLayer Intelligent Contracts

Provides easy-to-use functions for contracts to interact with external APIs:
- Weather data (Open-Meteo) — no API key
- Crypto prices (CoinGecko) — no API key
- JSON fetching / HTML scraping — generic
- News / RSS feeds / Hacker News — no API key
- Social media / GitHub stats — no API key
- Time & utility helpers — pure Python

All API functions use gl.get_from_web() internally and return parsed data.
"""

__version__ = "0.2.0"

from .weather import get_weather, get_weather_forecast
from .crypto import get_price, get_prices, get_market_data
from .web import fetch_json, fetch_text, scrape_links, scrape_text
from .news import fetch_rss, hackernews_top, search_hackernews
from .social import github_repo, github_releases, github_commits, twitter_user_stats
from .utils import (
    timestamp_now,
    timestamp_to_iso,
    iso_to_timestamp,
    time_ago,
    format_number,
    format_usd,
    truncate_string,
    bytes_to_hex,
    hex_to_bytes,
)

__all__ = [
    # Weather
    "get_weather",
    "get_weather_forecast",
    # Crypto
    "get_price",
    "get_prices",
    "get_market_data",
    # Web
    "fetch_json",
    "fetch_text",
    "scrape_links",
    "scrape_text",
    # News
    "fetch_rss",
    "hackernews_top",
    "search_hackernews",
    # Social
    "github_repo",
    "github_releases",
    "github_commits",
    "twitter_user_stats",
    # Utils
    "timestamp_now",
    "timestamp_to_iso",
    "iso_to_timestamp",
    "time_ago",
    "format_number",
    "format_usd",
    "truncate_string",
    "bytes_to_hex",
    "hex_to_bytes",
]
