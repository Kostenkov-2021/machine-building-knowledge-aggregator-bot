from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from responses.request_messages import REQUEST_MESSAGES
from responses.keyboards import get_start_keyboard
from db import crud
from db.database import SessionLocal

from states.states import States


request_router = Router()


@request_router.message(F.text.casefold() == "новый запрос")
async def new_request(message: types.Message, state: FSMContext):
    await message.answer(text=REQUEST_MESSAGES["request_prompt"])
    await state.set_state(States.waiting_for_request_content)


@request_router.message(States.waiting_for_request_content)
async def save_request(message: types.Message, state: FSMContext):
    db = SessionLocal()
    tg_id = message.from_user.id
    user = crud.get_user(db, tg_id=tg_id)
    if not user:
        user = crud.create_user(db, tg_id=tg_id, tg_name=message.from_user.username)
    crud.create_knowledge_request(db, user_id=user.id, content=message.text)
    db.close()
    await message.answer(text=REQUEST_MESSAGES["thank_message"], reply_markup=get_start_keyboard())
    await state.clear()