# genlayer-apis

Standardized API helpers for [GenLayer](https://genlayer.com) Intelligent Contracts.

> Easily fetch weather data, crypto prices, and web content from your Intelligent Contracts — no API keys, no boilerplate.

## Features

| Module | Description | API Key Required |
|--------|-------------|-----------------|
| `weather` | Current weather + forecasts (Open-Meteo) | No |
| `crypto` | Crypto prices + market data (CoinGecko) | No |
| `web` | Fetch JSON, scrape HTML | No |

## Installation

```bash
pip install genlayer-apis
```

## Quick Start

### Weather

```python
from genlayer_apis import get_weather, get_weather_forecast

# Current weather
weather = get_weather("Jakarta")
# {'city': 'Jakarta', 'country': 'Indonesia', 'temperature_c': 28.5, ...}

# 5-day forecast
forecast = get_weather_forecast("Tokyo", days=5)
```

### Crypto Prices

```python
from genlayer_apis import get_price, get_prices, get_market_data

btc = get_price("BTC")
# {'symbol': 'BTC', 'price': 87500.0, 'market_cap': 1730000000000, ...}

prices = get_prices(["BTC", "ETH", "SOL"])

eth = get_market_data("ETH")
```

### Web Scraping

```python
from genlayer_apis import fetch_json, fetch_text, scrape_links

data = fetch_json("https://api.example.com/data")
links = scrape_links("https://news.ycombinator.com", filter_pattern="github.com")
```

## Usage in Intelligent Contracts

GenLayer contracts must be self-contained (single file). Copy the helper functions directly into your contract class:

```python
import genlayer as gl
import json


class WeatherContract(gl.Contract):
    """Example: Weather-based decision contract."""

    COIN_IDS = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana"}

    def __init__(self):
        pass

    def _get_weather(self, city: str) -> dict:
        """Fetch weather using Open-Meteo (free, no API key)."""
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_data = json.loads(gl.get_from_web(url=geo_url, mode="raw"))

        if not geo_data.get("results"):
            raise ValueError(f"City not found: {city}")

        loc = geo_data["results"][0]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['latitude']}&longitude={loc['longitude']}&current_weather=true"
        weather_data = json.loads(gl.get_from_web(url=weather_url, mode="raw"))
        current = weather_data["current_weather"]

        return {
            "city": loc.get("name", city),
            "temperature_c": current["temperature"],
            "windspeed_kmh": current["windspeed"],
        }

    def _get_price(self, symbol: str) -> dict:
        """Fetch crypto price using CoinGecko (free, no API key)."""
        coin_id = self.COIN_IDS.get(symbol.upper(), symbol.lower())
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_market_cap=true"
        data = json.loads(gl.get_from_web(url=url, mode="raw"))

        if coin_id not in data:
            raise ValueError(f"Coin not found: {symbol}")

        return {
            "symbol": symbol.upper(),
            "price": data[coin_id].get("usd", 0),
            "market_cap": data[coin_id].get("usd_market_cap", 0),
        }

    @gl.public
    @gl.view
    def get_weather(self, city: str) -> str:
        w = self._get_weather(city)
        return f"{w['city']}: {w['temperature_c']}C, wind {w['windspeed_kmh']} km/h"

    @gl.public
    @gl.view
    def get_price(self, symbol: str) -> str:
        p = self._get_price(symbol)
        return f"{p['symbol']}: ${p['price']:,.2f}"
```

## API Reference

### `weather.get_weather(city, country_code="")`

Get current weather for a city.

**Returns:** `{city, country, latitude, longitude, temperature_c, windspeed_kmh, weathercode, time}`

### `weather.get_weather_forecast(city, days=3, country_code="")`

Get daily forecast for a city (1-16 days).

**Returns:** `[{date, temp_max_c, temp_min_c, precipitation_mm, weathercode}, ...]`

### `crypto.get_price(symbol, vs_currency="usd")`

Get current price for a cryptocurrency.

**Returns:** `{symbol, price, market_cap, volume_24h, change_24h_pct}`

### `crypto.get_prices(symbols, vs_currency="usd")`

Get prices for multiple cryptocurrencies.

**Returns:** `[{symbol, price, market_cap, volume_24h, change_24h_pct}, ...]`

### `crypto.get_market_data(symbol, vs_currency="usd")`

Get detailed market data.

**Returns:** `{symbol, name, price, market_cap, volume_24h, change_1h_pct, change_24h_pct, change_7d_pct, change_30d_pct, ath, ath_date, circulating_supply, total_supply}`

### `web.fetch_json(url)`

Fetch and parse JSON.

### `web.fetch_text(url)`

Fetch raw text/HTML.

### `web.scrape_links(url, filter_pattern="")`

Extract links from HTML, optionally filtered by regex.

### `web.scrape_text(url, tag="body")`

Extract text content from HTML element.

## Supported Coins

`BTC`, `ETH`, `SOL`, `BNB`, `XRP`, `ADA`, `DOGE`, `DOT`, `AVAX`, `MATIC`, `LINK`, `UNI`, `ARB`, `OP`, `GL`

You can also pass any CoinGecko coin ID directly.

## Tested On

- ✅ API calls verified locally (Open-Meteo, CoinGecko)
- ✅ Deployed on GenLayer Bradbury Testnet (status: ACCEPTED)
- ⚠️ Contract calls blocked by testnet RPC state issue (not a library bug)
- ✅ 12 unit tests passing

## License

MIT
