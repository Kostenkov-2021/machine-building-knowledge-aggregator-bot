from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from responses.response_messages import RESPONSE_MESSAGES
from responses.keyboards import get_start_keyboard
from db import crud
from db.database import SessionLocal

from states.states import States


answer_router = Router()


@answer_router.callback_query(F.data.startswith("addresponse_"))
async def add_response(callback: types.CallbackQuery, state: FSMContext):
    request_id = int(callback.data.split("_")[1])
    await state.update_data(request_id=request_id)
    await state.set_state(States.waiting_for_response_content)
    await callback.message.answer(RESPONSE_MESSAGES["response_prompt"])


@answer_router.message(States.waiting_for_response_content)
async def save_response(message: types.Message, state: FSMContext):
    data= await state.get_data()
    request_id = data["request_id"]
    tg_id = message.from_user.id
    db = SessionLocal()
    user = crud.get_user(db, tg_id=tg_id)
    if not user:
        user = crud.create_user(
            db, tg_id=tg_id, tg_name=message.from_user.username)
    crud.add_response_to_request(db, user_id=user.id, request_id=request_id, content=message.text)
    db.close()
    await message.answer(RESPONSE_MESSAGES["thank_response_message"], reply_markup=get_start_keyboard())
    await state.clear()
