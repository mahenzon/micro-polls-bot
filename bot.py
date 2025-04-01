from aiogram import Bot
from core.config import settings


def create_bot() -> Bot:
    bot = Bot(
        token=settings.telegram_api_token,
    )
    return bot
