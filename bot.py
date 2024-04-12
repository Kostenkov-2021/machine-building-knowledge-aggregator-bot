import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.exceptions import AiogramError

from handlers.start import start_router
from handlers.knowledge_request import request_router
from handlers.view_requests import view_requests_router
from handlers.view_responses import view_responses_router
from handlers.answer_request import answer_router
from handlers.search_by_tags import search_router


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение API токена из переменной окружения
API_TOKEN = os.getenv("MBKA_API_TOKEN")

# Проверка наличия токена
if not API_TOKEN:
    logger.error("API token is not set. Please set the MBKA_API_TOKEN environment variable.")
    raise ValueError("API token is not set. Please set the MBKA_API_TOKEN environment variable.")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)

# Регистрация роутеров
dp.include_router(start_router)
dp.include_router(request_router)
dp.include_router(view_requests_router)
dp.include_router(view_responses_router)
dp.include_router(answer_router)

if __name__ == "__main__":
    try:
        logger.info("Starting bot")
        dp.start_polling(bot)
    except AiogramException as e:
        logger.error(f"Error starting bot: {e}")
