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

Or add to your Intelligent Contract dependencies.

## Quick Start

### Weather

```python
from genlayer_apis import get_weather, get_weather_forecast

# Current weather
weather = get_weather("Jakarta")
# {'city': 'Jakarta', 'country': 'Indonesia', 'temperature_c': 28.5, ...}

# 5-day forecast
forecast = get_weather_forecast("Tokyo", days=5)
# [{'date': '2026-03-30', 'temp_max_c': 18.2, 'temp_min_c': 10.1, ...}, ...]
```

### Crypto Prices

```python
from genlayer_apis import get_price, get_prices, get_market_data

# Single price
btc = get_price("BTC")
# {'symbol': 'BTC', 'price': 87500.0, 'market_cap': 1730000000000, ...}

# Multiple prices
prices = get_prices(["BTC", "ETH", "SOL"])

# Detailed market data
eth = get_market_data("ETH")
# {'symbol': 'ETH', 'name': 'Ethereum', 'price': 3200.0, 'change_7d_pct': 5.3, ...}
```

### Web Scraping

```python
from genlayer_apis import fetch_json, fetch_text, scrape_links

# Fetch API response
data = fetch_json("https://api.example.com/data")

# Extract links from a page
links = scrape_links("https://news.ycombinator.com", filter_pattern="github.com")
```

## Example: Weather-Based Betting Contract

```python
import genlayer as gl
from genlayer_apis import get_weather, get_price

class WeatherBet(gl.Contract):
    def __init__(self, city: str, threshold_c: float):
        self.city = city
        self.threshold_c = threshold_c
        self.resolved = False

    @gl.public
    def check_weather(self) -> dict:
        weather = get_weather(self.city)
        self.result = "hot" if weather["temperature_c"] > self.threshold_c else "cold"
        self.resolved = True
        return {"city": weather["city"], "temperature": weather["temperature_c"], "result": self.result}
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

## License

MIT
