import asyncio
import re
from typing import Annotated

import httpx
from bs4 import BeautifulSoup
from httpx import Response

from app.bot.utils.logger import logger

__all__ = ["logger"]

SEPARATOR = "-" * 47

# Описание по баллам общей облачности
CLOUDS_BY_POINTS: dict[int, str] = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Преимущественно ясно",
    3: "Переменная облачность",
    4: "Переменная облачность",
    5: "Облачно",
    6: "Облачно",
    7: "Значительная облачность",
    8: "Значительная облачность",
    9: "Пасмурно",
    10: "Пасмурно",
}

# Типы облаков, при которых возможен дождь
RAIN_CLOUDS = ("Cb", "Ns")

_client: Annotated[
    httpx.AsyncClient | None, "Асинхронный клиент для отправки http запросов"
] = None

_client_lock: asyncio.Lock = asyncio.Lock()

semaphore: Annotated[asyncio.Semaphore, "Ограничитель запросов к API"] = (
    asyncio.Semaphore(3)
)


class HTTPClient:
    def __init__(self) -> None:
        self._timeout = httpx.Timeout(connect=40.0, read=30.0, write=10.0, pool=5.0)
        self._limits = httpx.Limits(
            max_connections=100, max_keepalive_connections=25, keepalive_expiry=30.0
        )
        self._transport: Annotated[
            httpx.AsyncHTTPTransport, "Добавление Retries для повторных запросов"
        ] = httpx.AsyncHTTPTransport(retries=3)

    async def __aenter__(self) -> httpx.AsyncClient:
        global _client
        async with _client_lock:
            if _client is None:
                _client = httpx.AsyncClient(
                    timeout=self._timeout,
                    limits=self._limits,
                    transport=self._transport,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/150.0.0.0 YaBrowser/26.8.0.0 Safari/537.36"
                        )
                    },
                )

            return _client

    async def __aexit__(self, *args: str) -> None:
        global _client
        async with _client_lock:
            if _client:
                await _client.aclose()
                _client = None


class APIClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def send_request(self, method: str, url: str) -> Response:
        logger.info(f"Производится отправка [GET] запроса на: {url}")
        try:
            response = await self.client.request(method, url)
            response.raise_for_status()
            return response
        except httpx.ConnectError as error:
            logger.error(f"Не удалось установить соединение с API.\nПричина: {error}")
            raise
        except httpx.TimeoutException:
            logger.error("Время на подключение к серверу истекло.")
            raise
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 503:
                logger.error(f"Сервис временно недоступен: {error}")
            else:
                logger.error(f"HTTP ошибка: {error}")
            raise

    @staticmethod
    def _clouds_to_text(clouds_raw: str) -> str:
        clouds_raw = clouds_raw.strip()

        # "ясно" — без баллов
        if clouds_raw.lower() == "ясно":
            return "Ясно"

        # Извлекаем баллы: "3/3 600 м [Sc]" → 3
        match = re.match(r"^(\d+)/", clouds_raw)
        if not match:
            return "Неизвестно"

        points = int(match.group(1))
        description = CLOUDS_BY_POINTS.get(points, "Неизвестно")

        # Проверяем, есть ли дождевые облака
        if any(rain_cloud in clouds_raw for rain_cloud in RAIN_CLOUDS):
            description += " (возможен дождь)"

        return description

    async def _fetch_data(self, response: Response) -> dict[str, str]:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")

        for row in reversed(rows):
            cells = row.find_all("td")
            if len(cells) < 13:
                continue

            temperature = cells[5].text.strip()
            if not temperature.startswith(("+", "-")):
                continue

            return {
                "temperature": temperature,
                "humidity": cells[7].text.strip(),
                "wind_dir": cells[0].text.strip(),
                "wind_speed": cells[1].text.strip(),
                "clouds": self._clouds_to_text(cells[4].text.strip()),
                "description": cells[10].text.strip(),
            }

        raise ValueError("Не удалось найти данные о погоде в HTML")

    async def _formatter_weather(self, data: Response) -> str:
        data_weather = await self._fetch_data(data)

        lines_data = [
            f"\n{SEPARATOR}",
            "🌤️  ПОГОДА В СЕВАСТОПОЛЕ",
            SEPARATOR,
            f"🌡️  Температура: {data_weather['temperature']}°C",
            f"💨  Ветер: {data_weather['wind_dir']} {data_weather['wind_speed']} м/с",
            f"💧  Влажность: {data_weather['humidity']}%",
            f"☁️  Погода: {data_weather['clouds']}",
            SEPARATOR,
        ]
        return "\n".join(lines_data)

    async def get_weather(self, data: Response) -> str:
        return await self._formatter_weather(data)


async def get_weather_today(url: str) -> str:
    async with HTTPClient() as client:
        api_client = APIClient(client)
        response = await api_client.send_request("GET", url)
        result = await api_client.get_weather(response)

    return result
