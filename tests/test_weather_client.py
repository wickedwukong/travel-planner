import os

import httpx
from journal.models import Weather
import pytest

class WeatherAPIClient:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    async def weather(self, city: str) -> Weather:
        url = f"{self.base_url.rstrip('/')}/v1/current.json?key={self.api_key}&q={city}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        weather_json = response.json()

        return Weather(
            city=weather_json["location"]["name"],
            description=weather_json["current"]["condition"]["text"],
            temperature=weather_json["current"]["temp_c"],
        )


@pytest.mark.asyncio
async def test_weather_client() -> None:
    weather_api_key: str = os.environ["WEATHER_API_KEY"]
    weather_api_client: WeatherAPIClient = WeatherAPIClient(api_key=weather_api_key, base_url="https://api.weatherapi.com")

    weather = await weather_api_client.weather("London")

    assert weather.city == "London"
    assert weather.temperature is not None
    assert weather.description is not None
