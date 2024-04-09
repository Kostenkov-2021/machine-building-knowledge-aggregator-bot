from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from responses.response_messages import RESPONSE_MESSAGES
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


@answer_router.message(state=States.waiting_for_response_content)
async def save_response(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        request_id = data["request_id"]
    db = SessionLocal()
    crud.create_response(db, request_id, message.text)
    db.close()
    await message.answer(RESPONSE_MESSAGES["thank_response_message"])
    await state.clear()
