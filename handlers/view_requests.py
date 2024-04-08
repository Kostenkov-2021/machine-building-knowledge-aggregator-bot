from aiogram import types, Router, F

from responses.request_messages import REQUEST_MESSAGES

from db import crud
from db.database import SessionLocal


view_requests_router = Router()


@view_requests_router.message(F.text.casefold() == "просмотреть запросы")
async def view_requests(message: types.Message):
    await message.answer(text="NotImplemented")
