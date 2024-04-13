import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from handlers.start import start_router
from handlers.knowledge_request import request_router
from handlers.view_requests import view_requests_router
from handlers.answer_request import answer_router

API_TOKEN = os.getenv("MBKA_API_TOKEN", "forgot")
if API_TOKEN=="forgot":
    API_TOKEN=input("enter token: ")
    os.environ["MBKA_API_TOKEN"]=API_TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)

dp.include_router(start_router)
dp.include_router(request_router)
dp.include_router(view_requests_router)
dp.include_router(answer_router)