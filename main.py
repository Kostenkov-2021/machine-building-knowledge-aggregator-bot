import logging
import asyncio

from aiogram.utils import executor

# from handlers import ...   # TODO
from bot import dp


logging.basicConfig(level=logging.DEBUG)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
