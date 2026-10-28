import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.configs.bot_config import settings_bot
from app.bot.handlers.commands import router

from loguru import logger

dp = Dispatcher()

bot = Bot(
    token=settings_bot.get_bot_token(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.include_router(router)

async def main() -> None:
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
