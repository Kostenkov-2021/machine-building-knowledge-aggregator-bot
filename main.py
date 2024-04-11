import logging
import asyncio

from handlers.start import start_router
from handlers.knowledge_request import request_router
from handlers.view_requests import view_requests_router
from handlers.answer_request import answer_router
from bot import dp

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

async def main() -> None:
    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(request_router)
    dp.include_router(view_requests_router)
    dp.include_router(answer_router)

    # Запуск поллинга
    await dp.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting!")
