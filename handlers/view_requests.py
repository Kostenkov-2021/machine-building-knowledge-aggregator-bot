from aiogram import types, Router, F

from responses.request_messages import REQUEST_MESSAGES
from responses.keyboards import get_start_keyboard, get_requests_keyboard, get_request_actions_keyboard

from db import crud
from db.database import SessionLocal


view_requests_router = Router()


@view_requests_router.message(F.text.casefold() == "просмотреть запросы")
async def view_requests(message: types.Message):
    db = SessionLocal()
    requests = crud.get_knowledge_requests(db)

    if not requests:
        await message.answer(REQUEST_MESSAGES["no_requests_message"], reply_markup=get_start_keyboard())
        db.close()
        return

    keyboard = get_requests_keyboard(requests)
    db.close()
    await message.answer(REQUEST_MESSAGES["view_requests_prompt"], reply_markup=keyboard)


@view_requests_router.callback_query(F.data.startswith("request_"))
async def view_request(callback: types.CallbackQuery):
    request_id = int(callback.data.split("_")[1])
    db = SessionLocal()
    request = crud.get_knowledge_request(db, request_id)
    db.close()

    await callback.message.answer(request.content, reply_markup=get_request_actions_keyboard(request_id))