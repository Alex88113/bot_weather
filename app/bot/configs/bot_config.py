from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr



class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, env_file_encoding="utf-8", extra="ignore"
    )

    WEATHER_API_URL: str
    BOT_TOKEN: SecretStr = Field(min_length=20, description="Bot token")

    def get_bot_token(self) -> str:
        return self.BOT_TOKEN.get_secret_value()


@lru_cache(maxsize=1)
def get_settings_bot() -> BotConfig:
    return BotConfig()


settings_bot = get_settings_bot()
print(settings_bot)
