"""
Crypto price API helpers using CoinGecko (free, no API key for basic usage).

https://www.coingecko.com/en/api
"""

import json
import genlayer.gl as gl


# Common coin ID mappings
COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "DOT": "polkadot",
    "AVAX": "avalanche-2",
    "MATIC": "matic-network",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "ARB": "arbitrum",
    "OP": "optimism",
    "GL": "genlayer",  # placeholder — update when listed
}


def _resolve_coin_id(symbol: str) -> str:
    """Resolve a symbol like 'BTC' to CoinGecko ID."""
    upper = symbol.upper()
    if upper in COIN_IDS:
        return COIN_IDS[upper]
    # Assume it's already a CoinGecko ID
    return symbol.lower()


def get_price(symbol: str, vs_currency: str = "usd") -> dict:
    """
    Get current price of a cryptocurrency.

    :param symbol: Coin symbol (e.g. "BTC", "ETH") or CoinGecko ID
    :param vs_currency: Target currency (default "usd")
    :returns: dict with keys: symbol, price, market_cap, volume_24h, change_24h_pct

    Example::

        btc = get_price("BTC")
        # {'symbol': 'BTC', 'price': 87500.0, 'market_cap': 1730000000000, ...}
    """
    coin_id = _resolve_coin_id(symbol)

    url = (
        f"https://api.coingecko.com/api/v3/simple/price?"
        f"ids={coin_id}"
        f"&vs_currencies={vs_currency}"
        f"&include_market_cap=true"
        f"&include_24hr_vol=true"
        f"&include_24hr_change=true"
    )

    response = gl.get_from_web(url=url, mode="raw")
    data = json.loads(response)

    if coin_id not in data:
        raise ValueError(f"Coin not found: {symbol} (id: {coin_id})")

    coin_data = data[coin_id]

    return {
        "symbol": symbol.upper(),
        "price": coin_data.get(vs_currency, 0),
        "market_cap": coin_data.get(f"{vs_currency}_market_cap", 0),
        "volume_24h": coin_data.get(f"{vs_currency}_24h_vol", 0),
        "change_24h_pct": coin_data.get(f"{vs_currency}_24h_change", 0),
    }


def get_prices(symbols: list[str], vs_currency: str = "usd") -> list[dict]:
    """
    Get current prices for multiple cryptocurrencies.

    :param symbols: List of coin symbols (e.g. ["BTC", "ETH", "SOL"])
    :param vs_currency: Target currency (default "usd")
    :returns: list of dicts, same format as get_price()

    Example::

        prices = get_prices(["BTC", "ETH", "SOL"])
        # [{'symbol': 'BTC', 'price': 87500.0, ...}, ...]
    """
    coin_ids = [_resolve_coin_id(s) for s in symbols]
    ids_str = ",".join(coin_ids)

    url = (
        f"https://api.coingecko.com/api/v3/simple/price?"
        f"ids={ids_str}"
        f"&vs_currencies={vs_currency}"
        f"&include_market_cap=true"
        f"&include_24hr_vol=true"
        f"&include_24hr_change=true"
    )

    response = gl.get_from_web(url=url, mode="raw")
    data = json.loads(response)

    result = []
    for symbol, coin_id in zip(symbols, coin_ids):
        if coin_id not in data:
            result.append({"symbol": symbol.upper(), "error": "not found"})
            continue

        coin_data = data[coin_id]
        result.append({
            "symbol": symbol.upper(),
            "price": coin_data.get(vs_currency, 0),
            "market_cap": coin_data.get(f"{vs_currency}_market_cap", 0),
            "volume_24h": coin_data.get(f"{vs_currency}_24h_vol", 0),
            "change_24h_pct": coin_data.get(f"{vs_currency}_24h_change", 0),
        })

    return result


def get_market_data(symbol: str, vs_currency: str = "usd") -> dict:
    """
    Get detailed market data for a cryptocurrency.

    :param symbol: Coin symbol or CoinGecko ID
    :param vs_currency: Target currency (default "usd")
    :returns: dict with keys: symbol, name, price, market_cap, volume_24h,
              change_1h_pct, change_24h_pct, change_7d_pct, change_30d_pct,
              ath, ath_date, circulating_supply, total_supply

    Example::

        data = get_market_data("ETH")
        # {'symbol': 'ETH', 'name': 'Ethereum', 'price': 3200.0, ...}
    """
    coin_id = _resolve_coin_id(symbol)

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false"

    response = gl.get_from_web(url=url, mode="raw")
    data = json.loads(response)

    market = data.get("market_data", {})

    return {
        "symbol": symbol.upper(),
        "name": data.get("name", ""),
        "price": market.get("current_price", {}).get(vs_currency, 0),
        "market_cap": market.get("market_cap", {}).get(vs_currency, 0),
        "volume_24h": market.get("total_volume", {}).get(vs_currency, 0),
        "change_1h_pct": market.get("price_change_percentage_1h_in_currency", {}).get(vs_currency, 0),
        "change_24h_pct": market.get("price_change_percentage_24h", 0),
        "change_7d_pct": market.get("price_change_percentage_7d", 0),
        "change_30d_pct": market.get("price_change_percentage_30d", 0),
        "ath": market.get("ath", {}).get(vs_currency, 0),
        "ath_date": market.get("ath_date", {}).get(vs_currency, ""),
        "circulating_supply": market.get("circulating_supply", 0),
        "total_supply": market.get("total_supply", 0),
    }
