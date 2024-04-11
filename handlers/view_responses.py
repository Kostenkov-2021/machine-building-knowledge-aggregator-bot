# for now, copypasted from view_requests.py
from aiogram import types, Router, F

from responses.response_messages import RESPONSE_MESSAGES
from responses.keyboards import get_start_keyboard, get_responses_keyboard, get_response_actions_keyboard

from db import crud
from db.database import SessionLocal


view_responses_router = Router()


@view_responses_router.callback_query(F.data.startswith("viewresponse_"))
async def view_responses(callback: types.CallbackQuery):
    request_id = int(callback.data.split("_")[1])
    db = SessionLocal()
    responses = crud.get_responses_for_request(db, request_id)
    if not responses:
        await callback.message.answer(RESPONSE_MESSAGES["no_responses_message"], reply_markup=get_start_keyboard())
        db.close()
        return

    keyboard = get_responses_keyboard(responses)
    db.close()
    await callback.message.answer(RESPONSE_MESSAGES["view_responses_prompt"], reply_markup=keyboard)


@view_responses_router.callback_query(F.data.startswith("response_"))
async def view_response(callback: types.CallbackQuery):
    response_id = int(callback.data.split("_")[1])
    print(response_id)
    db = SessionLocal()
    response = crud.get_response(db, response_id)
    db.close()
    await callback.message.answer(response.content, reply_markup=get_response_actions_keyboard(response_id))


