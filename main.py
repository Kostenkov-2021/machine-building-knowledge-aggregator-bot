import logging
import asyncio

from bot import dp

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

async def main() -> None:
    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(request_router)
    dp.include_router(view_requests_router)
    dp.include_router(answer_router)

@dp.message_handler(content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.VOICE])
async def handle_message(message: types.Message):
    if message.content_type == 'text':
        create_knowledge_request(session, user_id=message.from_user.id, content=message.text)
    else:
        file_id = message.photo[-1].file_id if message.content_type == 'photo' else message[message.content_type].file_id
        file_url = await bot.get_file_url(file_id)
        create_knowledge_request(session, user_id=message.from_user.id, content='', file_url=file_url, file_type=message.content_type)
    
    # Запуск поллинга
    await dp.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting!")
