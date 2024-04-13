from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from db import crud
from db.database import SessionLocal
from states.states import States

edit_router = Router()

@edit_router.callback_query(F.data.startswith("editrequest_"))
async def edit_request(callback: types.CallbackQuery, state: FSMContext):
    db = SessionLocal()
    requests = crud.edit_knowledge_request(db)
    await state.update_data(request_id=int(callback.data.split("_")[1]))
    await state.set_state(States.editing_request_content)
    await callback.message.answer("Введите новый текст запроса:")

@edit_router.message(States.editing_request_content)
async def save_edited_request(message: types.Message, state: FSMContext):
    data = await state.get_data()
    request_id = data["request_id"]
    await message.answer("Запрос успешно отредактирован.")
    await state.clear()
    return


@edit_router.callback_query(F.data.startswith("editresponse_"))
async def edit_response(callback: types.CallbackQuery, state: FSMContext):
    db = SessionLocal()
    requests = crud.edit_response(db)

    await state.update_data(response_id=int(callback.data.split("_")[1]))
    await state.set_state(States.editing_request_content)
    await callback.message.answer("Введите новый текст ответа:")

@edit_router.message(States.editing_response_content)
async def save_edited_response(message: types.Message, state: FSMContext):
    data = await state.get_data()
    response_id = data["response_id"]
    await message.answer("Ответ успешно отредактирован.")
    return
