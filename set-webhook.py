import asyncio
import logging

from bot import create_bot
from core import settings

log = logging.getLogger(__name__)


async def main() -> None:
    bot = create_bot()
    log.warning("Me %s", await bot.get_me())
    log.warning("Delete webhook")
    await bot.delete_webhook()
    log.warning("Set webhook")
    await bot.set_webhook(
        url=settings.api_gateway_url,
    )
    log.warning("Done!")


if __name__ == "__main__":
    asyncio.run(main())
