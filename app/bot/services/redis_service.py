from redis.asyncio import ConnectionPool, Redis

from app.bot.utils.logger import logger
from app.bot.configs.bot_config import settings_bot


redis_client: Redis | None = None

class RedisClient:
    def __init__(
        self,
        host: str = settings_bot.REDIS_HOST,
        port: int = settings_bot.REDIS_PORT,
        decode_responses: bool = True,
        max_connections: int = 10,
        socket_connect_timeout: int = 20,
        socket_timeout: int = 15,
        retry_on_timeout: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.decode_responses = decode_responses
        self.max_connections = max_connections
        self.socket_connect_timeout = socket_connect_timeout
        self.socket_timeout = socket_timeout
        self.retry_on_timeout = retry_on_timeout

    async def __aenter__(self) -> Redis:
        logger.info("Подготавливаем Redis клиент")
        global redis_client
        if redis_client is None:
            pool = ConnectionPool.from_url(
                f"redis://{self.host}:{self.port}",
                max_connections=self.max_connections,
                decode_responses=self.decode_responses,
                socket_connect_timeout=self.socket_connect_timeout,
                socket_timeout=self.socket_timeout,
                retry_on_timeout=self.retry_on_timeout,
            )

            redis_client = Redis(connection_pool=pool)
            logger.info("Клиент создан.")
            logger.debug(f"Connect to redis is install, Port={self.port}, Host={self.host}")

        return redis_client

    async def __aexit__(self, *args: str) -> None:
        global redis_client
        if redis_client:
            await redis_client.aclose()
            redis_client = None
            logger.info("Клиент закрыт")
