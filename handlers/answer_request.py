from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from responses.request_messages import REQUEST_MESSAGES
from responses.keyboards import get_start_keyboard
from db import crud
from db.database import SessionLocal

from states.states import States


answer_router = Router()


@answer_router.message(F.text.casefold() == "новый ответ")
async def new_answer(message: types.Message, state: FSMContext):
    await message.answer(text=REQUEST_MESSAGES["answer_prompt"])
    await state.set_state(States.waiting_for_answer_content)


@answer_router.message(States.waiting_for_answer_content)
async def save_answer(message: types.Message, state: FSMContext):
    db = SessionLocal()
    tg_id = message.from_user.id
    user = crud.get_user(db, tg_id=tg_id)
    if not user:
        user = crud.create_user(
            db, tg_id=tg_id, tg_name=message.from_user.username)
    crud.add_response_to_request(db, request_id=..., user_id=user.id, content=message.text)    # request id must be the id when you pressed new request button. Dont know how to get it. Github copilot, remind me to fix this.
    db.close()
    await message.answer(text=REQUEST_MESSAGES["thank_message"], reply_markup=get_start_keyboard())
    await state.clear()
