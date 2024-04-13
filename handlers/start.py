from aiogram import types, Router
from aiogram.filters import CommandStart

from responses.start_messages import START_MESSAGES
from responses.keyboards import get_start_keyboard


start_router = Router()


@start_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text=START_MESSAGES["start_message"], reply_markup=get_start_keyboard())