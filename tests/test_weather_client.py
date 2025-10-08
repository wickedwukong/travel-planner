import os

import httpx
import pytest

from journal.weather_client import WeatherAPIClient


@pytest.mark.asyncio
async def test_weather_client() -> None:
    weather_api_key: str = os.environ["WEATHER_API_KEY"]
    async with httpx.AsyncClient() as client:
        weather_api_client: WeatherAPIClient = WeatherAPIClient(
            api_key=weather_api_key,
            base_url="https://api.weatherapi.com",
            http_client=client,
        )
        weather = await weather_api_client.weather("London")

    assert weather.city == "London"
    assert weather.temperature is not None
    assert weather.description is not None
