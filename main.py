import logging
import asyncio

from aiogram.types import ContentType, Message
from aiogram import F
from bot import dp

from db.crud import create_knowledge_request
from db.database import get_db
# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

async def main() -> None:
    # Запуск поллинга
    await dp.start_polling()


@dp.message(F.content_type == ContentType.TEXT or F.content_type == ContentType.VOICE or F.content_type == ContentType.PHOTO)
async def handle_message(message: Message):
    with get_db() as session:
        if message.content_type == 'text':
            create_knowledge_request(session, user_id=message.from_user.id, content=message.text)
        else:
            file_id = message.photo[-1].file_id if message.content_type == 'photo' else message[message.content_type].file_id
            file_url = await bot.get_file_url(file_id)
            create_knowledge_request(session, user_id=message.from_user.id, content='', file_url=file_url, file_type=message.content_type)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting!")
