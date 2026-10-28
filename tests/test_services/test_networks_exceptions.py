from collections.abc import AsyncGenerator

import respx
import pytest
from httpx import AsyncClient
import httpx

from app.bot.services.weather_service import HTTPClient, APIClient
from app.bot.configs.bot_config import settings_bot


@pytest.fixture
async def async_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with HTTPClient() as client:
        yield client


@pytest.fixture
async def return_api_client(async_http_client: AsyncClient) -> APIClient:
    api_client = APIClient(async_http_client)
    return api_client


@pytest.fixture
async def weather_url() -> str:
    return settings_bot.WEATHER_API_URL


class TestTimeoutException:
    @respx.mock
    async def test_timeout(self, return_api_client, weather_url) -> None:
        respx.get(weather_url).mock(side_effect=httpx.TimeoutException("timed out"))

        with pytest.raises(httpx.TimeoutException):
            await return_api_client.send_request("GET", weather_url)


class TestConnectError:
    @respx.mock
    async def test_connect_exception(self, return_api_client, weather_url) -> None:
        respx.get(weather_url).mock(side_effect=httpx.ConnectError("Mock Error"))

        with pytest.raises(httpx.ConnectError):
            await return_api_client.send_request("GET", weather_url)


class TestHTTPStatusError:
    @respx.mock
    async def test_http_status_503_error(
        self, return_api_client: APIClient, weather_url: str
    ) -> None:
        respx.get(weather_url).mock(return_value=httpx.Response(503))

        with pytest.raises(httpx.HTTPStatusError):
            await return_api_client.send_request("GET", weather_url)

    @respx.mock
    async def test_http_status_404_error(
        self, return_api_client: APIClient, weather_url: str
    ) -> None:
        respx.get(weather_url).mock(return_value=httpx.Response(404))

        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await return_api_client.send_request("GET", weather_url)
        assert exc_info.value.response.status_code == 404

    @respx.mock
    async def test_http_status_402_error(
        self, return_api_client: APIClient, weather_url: str
    ) -> None:
        respx.get(weather_url).mock(return_value=httpx.Response(402))

        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await return_api_client.send_request("GET", weather_url)
        assert exc_info.value.response.status_code == 402
