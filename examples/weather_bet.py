"""
Example: Weather-based betting contract using genlayer-apis

This Intelligent Contract resolves a bet based on weather data.
If the temperature in Jakarta exceeds 35°C, the bet resolves as "hot".
"""

import genlayer as gl
from genlayer_apis import get_weather, get_price


class WeatherBet(gl.Contract):
    city: str
    threshold_c: float
    crypto_symbol: str
    resolved: bool
    result: str

    def __init__(self, city: str, threshold_c: float, crypto_symbol: str):
        self.city = city
        self.threshold_c = threshold_c
        self.crypto_symbol = crypto_symbol
        self.resolved = False
        self.result = ""

    @gl.public
    def check_weather(self) -> dict:
        """Fetch current weather and check against threshold."""
        weather = get_weather(self.city)

        if weather["temperature_c"] > self.threshold_c:
            self.result = "hot"
        else:
            self.result = "cold"

        self.resolved = True
        return {
            "city": weather["city"],
            "temperature": weather["temperature_c"],
            "threshold": self.threshold_c,
            "result": self.result,
        }

    @gl.public
    def get_crypto_context(self) -> dict:
        """Get current crypto price alongside weather data."""
        weather = get_weather(self.city)
        price = get_price(self.crypto_symbol)

        return {
            "weather": weather,
            "crypto": price,
        }

    @gl.public
    @gl.view
    def get_result(self) -> str:
        return self.result if self.resolved else "not resolved"
