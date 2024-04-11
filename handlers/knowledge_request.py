from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from responses.request_messages import REQUEST_MESSAGES
from responses.keyboards import get_start_keyboard
from db import crud
from db.database import get_db

from states.states import States

request_router = Router()

@request_router.message(F.text.casefold() == "новый запрос")
async def new_request(message: types.Message, state: FSMContext):
    await message.answer(text=REQUEST_MESSAGES["request_prompt"])
    await state.set_state(States.waiting_for_request_content)

@request_router.message(States.waiting_for_request_content)
async def save_request(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    try:
        with get_db() as db:
            # Проверка существования пользователя и создание нового при необходимости
            user = crud.get_user(db, tg_id=tg_id)
            if not user:
                user = crud.create_user(db, tg_id=tg_id, tg_name=message.from_user.username)
            # Создание нового запроса
            crud.create_knowledge_request(db, user_id=user.id, content=message.text)
        
        # Уведомление пользователя об успешном создании запроса
        await message.answer(text=REQUEST_MESSAGES["thank_message"], reply_markup=get_start_keyboard())
    except Exception as e:
        # Логирование исключения и уведомление пользователя об ошибке
        await message.answer(text=REQUEST_MESSAGES["error_message"])
    finally:
        await state.clear()
