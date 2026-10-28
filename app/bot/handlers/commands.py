from aiogram import Router, types
from aiogram.filters import Command

from app.bot.configs.bot_config import settings_bot
from app.bot.services.weather_service import get_weather_today

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user_name = message.from_user.first_name or "друг"
    await message.answer(
        f"👋 Привет, <b>{user_name}</b>!\n\n"
        f"🌤️ Я бот для мониторинга погоды.\n"
        f"📍 Город: <b>Севастополь</b>\n\n"
        f"Напиши /help, чтобы увидеть команды."
    )

@router.message(Command("weather"))
async def extradition_weather_today(message: types.Message) -> None:
    await message.answer(await get_weather_today(settings_bot.WEATHER_API_URL))

@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    text_commands: list[str] = [
        "━━━━━━━━━━━━━━━━━━━━",
        "📋  СПИСОК КОМАНД",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "🚀 /start — приветствие",
        "🌤️ /weather — погода на сегодня",
        "❓ /help — этот список",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    await message.answer("\n".join(text_commands))
