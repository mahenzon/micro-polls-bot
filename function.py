import asyncio

from aiogram.types import Update
from bot import create_bot
from dispatcher import create_dispatcher


async def handle_update(update: Update):
    bot = create_bot()
    dp = create_dispatcher()
    return await dp.feed_update(bot, update)


def prepare_update(event: dict[str, dict]):
    return Update.model_validate(event["body"])


def handle(event, context):
    update = prepare_update(event)
    asyncio.run(handle_update(update))
    return {
        "statusCode": 204,
        "body": "",
    }
