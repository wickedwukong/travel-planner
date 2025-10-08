from journal.models import Weather
import httpx


class WeatherAPIClient:
    def __init__(
        self, api_key: str, base_url: str, http_client: httpx.AsyncClient
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.http_client = http_client

    async def weather(self, city: str) -> Weather:
        url = f"{self.base_url.rstrip('/')}/v1/current.json?key={self.api_key}&q={city}"

        response = await self.http_client.get(url)

        weather_json = response.json()

        return Weather(
            city=weather_json["location"]["name"],
            description=weather_json["current"]["condition"]["text"],
            temperature=weather_json["current"]["temp_c"],
        )
