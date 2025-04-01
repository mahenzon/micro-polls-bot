import asyncio
import logging

from bot import create_bot
from dispatcher import create_dispatcher

log = logging.getLogger(__name__)


async def run() -> None:
    bot = create_bot()
    dispatcher = create_dispatcher()

    await dispatcher.start_polling(bot)


def main():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )
    asyncio.run(run())


if __name__ == "__main__":
    main()
