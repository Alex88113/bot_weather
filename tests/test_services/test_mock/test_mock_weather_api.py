import pytest
from httpx import AsyncClient, Response
import respx
from respx import Route
import httpx
from app.bot.services.weather_service import HTTPClient, APIClient

type ResultType = None

class TestWeatherAPI:
    @pytest.fixture
    async def async_http_client(self):
        async with HTTPClient() as client:
            yield client
            
    @respx.mock
    async def test_send_request_get(self, async_http_client) -> ResultType:
        route: Route = respx.get('https://pogodaiklimat.ru/weather.php?id=33991').mock(return_value=Response(status_code=200))
        response: Response = await async_http_client.get("https://pogodaiklimat.ru/weather.php?id=33991")
        headers = response.headers
        response_format = ('text/html', 'json/application')
        
        assert route.called
        assert response.status_code == 200
        assert response is not None
        assert type(response) is Response
        assert any(headers for headers['content-type'] in response_format)
        
    @respx.mock
    async def test_send_request_succesful(self, async_http_client) -> ResultType:
        route = respx.get('https://pogodaiklimat.ru/weather.php?id=33991').mock(
            return_value=Response(status_code=200)
        )
        
        api_client: APIClient = APIClient(async_http_client)
        response: Response = await api_client.send_request('GET', 'https://pogodaiklimat.ru/weather.php?id=33991')
        
        assert route.called
        assert response.status_code == 200
        assert response is not None
        assert isinstance(response, Response)
        
    @pytest.mark.asyncio
    async def test_response_format(self, async_http_client: AsyncClient) -> ResultType:
        api_client = APIClient(async_http_client)
        response: Response = await api_client.send_request('GET', 'https://pogodaiklimat.ru/weather.php?id=33991')
        content_type = response.headers['content-type'].lower().split(';')[0].strip()
        allowed_formats = ('text/html', 'application/json')
        assert content_type in allowed_formats, (
            f"One of the API response formars was expected: {allowed_formats}, but the following was received: {content_type}"
        )

class TestException:
    @pytest.fixture
    async def async_http_client(self):
        async with HTTPClient() as client:
            yield client
    
    @pytest.mark.asyncio
    async def test_send_request_connect_error(self, async_http_client) -> ResultType:
        api_client = APIClient(async_http_client)
        
        with respx.mock:
            respx.get('https://pogodaiklimat.ru/weather.php?id=33991').mock(
                side_effect=httpx.ConnectError("Mock Error")
            )
            
            with pytest.raises(httpx.ConnectError, match='Mock Error') as excinfo:
                await api_client.send_request("GET", "https://pogodaiklimat.ru/weather.php?id=33991")
                
            assert f"Information about the exception that occurred: {excinfo.value}"
            
            