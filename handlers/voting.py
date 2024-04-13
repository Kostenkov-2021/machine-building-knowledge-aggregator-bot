from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from db.crud import add_vote_to_knowledge_request, add_vote_to_response
from states.states import States

vote_router = Router()

    @request_router.message(F.text.casefold() == "новый запрос")

async def vote_for_request(message: types.Message):
    # Извлекаем данные из сообщения
    request_id, user_id, vote = 1, message.from_user.id, 1
    add_vote_to_knowledge_request(session, request_id, user_id, vote)
    await message.reply("Ваш голос учтён.")

async def vote_for_response(message: types.Message):
    # Извлекаем данные из сообщения
    responce_id, user_id, vote = 1, message.from_user.id, 1
    add_vote_to_knowledge_request(session, request_id, user_id, vote)
    await message.reply("Ваш голос учтён.")

    pass

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(vote_for_request, commands=['vote_request'])
    dp.register_message_handler(vote_for_response, commands=['vote_response'])
