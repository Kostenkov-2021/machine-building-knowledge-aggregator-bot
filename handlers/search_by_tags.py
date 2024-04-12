from aiogram import types, Router
from aiogram.filters import Command

from db.database import get_db
from db.crud import get_requests_by_tag

search_router = Router()

@search_router.message(Command('search_by_tag'))
async def search_requests_by_tag(message: types.Message):
    tag_name = message.get_args()
    with get_db() as session:
        requests = get_requests_by_tag(session, tag_name)
    if not requests:
        await message.answer("Запросов с таким тегом не найдено.")
        return
    response_text = "\n".join(f"{request.id}: {request.content}" for request in requests)
    await message.answer(response_text)
