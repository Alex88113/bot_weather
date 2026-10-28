from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient, Response
import httpx

from app.bot.services.weather_service import HTTPClient
from app.bot.configs.bot_config import settings_bot


@pytest.fixture
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    async with HTTPClient() as client:
        yield client

class TestHTTPClient:
    @pytest.mark.asyncio
    async def test_created_http_client(self, http_client: AsyncClient) -> None:
        assert http_client is not None
        assert isinstance(http_client, httpx.AsyncClient)
        assert str(http_client.base_url) == settings_bot.WEATHER_API_URL
        assert "User-Agent" in http_client.headers

    @pytest.mark.asyncio
    async def test_closed_client(self) -> None:
        async with HTTPClient() as client:
            assert client is not None
            assert isinstance(client, httpx.AsyncClient)
            assert str(client.base_url) == settings_bot.WEATHER_API_URL
            assert "User-Agent" in client.headers

        assert client.is_closed

    @pytest.mark.asyncio
    async def test_work_http_client(self, http_client: AsyncClient) -> None:
        response = await http_client.get(settings_bot.WEATHER_API_URL)
        content_type = response.headers["content-type"].lower().split(";")[0].strip()
        allowed_formats = ("text/html", "application/json")

        assert response is not None
        assert isinstance(response, Response)
        assert response.status_code == 200
        assert content_type in allowed_formats, (
            f"One of the API response formats was expected: {allowed_formats}, but the following was received: {content_type}"
        )
