import logging
import asyncio

from handlers import *

from bot import bot, dp


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting!")