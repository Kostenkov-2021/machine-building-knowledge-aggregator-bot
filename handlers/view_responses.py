# for now, copypasted from view_requests.py
from aiogram import types, Router, F
import logging

from responses.response_messages import RESPONSE_MESSAGES
from responses.keyboards import get_start_keyboard, get_responses_keyboard, get_response_actions_keyboard

from db import crud
from db.database import SessionLocal

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

view_responses_router = Router()

@view_responses_router.message(F.text.casefold() == "просмотреть ответы")
async def view_responses(message: types.Message):
    db = SessionLocal()
    responses = crud.get_responses(db)

    if not responses:
        await message.answer(RESPONSE_MESSAGES["no_responses_message"], reply_markup=get_start_keyboard())
        db.close()
        return

    keyboard = get_responses_keyboard(responses)
    db.close()
    await message.answer(RESPONSE_MESSAGES["view_responses_prompt"], reply_markup=keyboard)


@view_responses_router.callback(F.data.startswith("response_"))
async def view_response(callback: types.CallbackQuery):
    response_id = int(callback.data.split("_")[1])
    db = SessionLocal()
    response = crud.get_response(db, response_id)
    db.close()
    await callback.message.answer(response.content, reply_markup=get_response_actions_keyboard(response_id))


