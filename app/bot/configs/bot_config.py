from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, ValidationError
from loguru import logger
from dotenv import load_dotenv

from app.bot.services.exceptions import ValidationEnvError

load_dotenv()

class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, env_file_encoding="utf-8", extra="ignore"
    )

    WEATHER_API_URL: str
    BOT_TOKEN: SecretStr

    def get_bot_token(self) -> str:
        return self.BOT_TOKEN.get_secret_value()


@lru_cache(maxsize=1)
def get_settings_bot() -> BotConfig:
    return BotConfig() # type: ignore[call-arg]

try:
    settings_bot = get_settings_bot()
    logger.debug("Конфиг с настройками из .env загружен")
except ValidationError as error:
    logger.error(f'Поймано исключение при загрузке переменных из .env: {ValidationEnvError(str(error))}')
    raise