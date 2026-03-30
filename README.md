# genlayer-apis

Standardized API helpers for [GenLayer](https://genlayer.com) Intelligent Contracts.

> Easily fetch weather data, crypto prices, news, GitHub stats, and web content from your Intelligent Contracts — no API keys, no boilerplate.

## Features

| Module | Description | API Key |
|--------|-------------|---------|
| `weather` | Current weather + forecasts (Open-Meteo) | No |
| `crypto` | Crypto prices + market data (CoinGecko) | No |
| `web` | Fetch JSON, scrape HTML | No |
| `news` | RSS feeds + Hacker News top/search | No |
| `social` | GitHub repos/releases/commits, Twitter stats | No |
| `utils` | Timestamps, formatting, hex encoding | Pure Python |

## Installation

```bash
pip install genlayer-apis
```

## Quick Start

### Weather

```python
from genlayer_apis import get_weather, get_weather_forecast

weather = get_weather("Jakarta")
# {'city': 'Jakarta', 'country': 'Indonesia', 'temperature_c': 28.5, ...}

forecast = get_weather_forecast("Tokyo", days=5)
```

### Crypto Prices

```python
from genlayer_apis import get_price, get_prices, get_market_data

btc = get_price("BTC")
# {'symbol': 'BTC', 'price': 87500.0, 'market_cap': 1730000000000, ...}

multiple = get_prices(["BTC", "ETH", "SOL"])

detailed = get_market_data("ETH")
# {'symbol': 'ETH', 'name': 'Ethereum', 'ath': 4878.0, ...}
```

### News & Hacker News

```python
from genlayer_apis import fetch_rss, hackernews_top, search_hackernews

# Fetch BBC News RSS
news = fetch_rss("https://feeds.bbci.co.uk/news/rss.xml", max_items=5)

# Hacker News top stories
top = hackernews_top(max_items=10)
# [{'title': 'Show HN: ...', 'score': 250, ...}, ...]

# Search Hacker News
results = search_hackernews("genlayer")
```

### GitHub Stats

```python
from genlayer_apis import github_repo, github_releases, github_commits

# Repository info
info = github_repo("genlayerlabs", "genvm")
# {'name': 'genvm', 'stars': 150, 'language': 'Rust', ...}

# Latest releases
releases = github_releases("genlayerlabs", "genvm")

# Recent commits
commits = github_commits("genlayerlabs", "genvm")
```

### Web Scraping

```python
from genlayer_apis import fetch_json, fetch_text, scrape_links, scrape_text

data = fetch_json("https://api.example.com/data")
links = scrape_links("https://news.ycombinator.com", filter_pattern="github.com")
text = scrape_text("https://example.com", tag="p")
```

### Utilities

```python
from genlayer_apis import timestamp_now, time_ago, format_usd, bytes_to_hex

ts = timestamp_now()  # 1711800000
ago = time_ago(ts - 3600)  # "1 hours ago"
price = format_usd(1234.5)  # "$1,234.50"
hex_str = bytes_to_hex(b"\xde\xad")  # "0xdead"
```

## Usage in Intelligent Contracts

```python
from genlayer import Contract
from genlayer_apis import get_weather, get_price, github_repo

class WeatherBet(Contract):
    def __init__(self):
        self.bets = []

    def bet_temperature(self, city: str, predicted: float):
        """Bet on the temperature of a city."""
        self.bets.append({"city": city, "predicted": predicted, "bettor": msg.sender})

    def resolve(self) -> dict:
        """Resolve all bets using current weather data."""
        results = []
        for bet in self.bets:
            weather = get_weather(bet["city"])
            actual = weather["temperature_c"]
            results.append({
                "city": bet["city"],
                "predicted": bet["predicted"],
                "actual": actual,
                "winner": abs(bet["predicted"] - actual) < 2,
            })
        return {"results": results}
```

## Tested On

- **Bradbury Testnet** — All API calls verified working
- **Python 3.12+**

## Contributing

This library is part of GenLayer's contribution quests. PRs welcome!
