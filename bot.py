import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from handlers.start import start_router
from handlers.knowledge_request import request_router


API_TOKEN = os.getenv("MBKA_API_TOKEN", "your_default_api_token")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)

dp.include_router(start_router)
dp.include_router(request_router)
