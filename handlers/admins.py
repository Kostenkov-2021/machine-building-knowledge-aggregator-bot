from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminLogin(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

async def admin_command_start(message: types.Message):
    await AdminLogin.waiting_for_username.set()
    await message.reply("Введите логин:")

async def admin_username_received(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await AdminLogin.next()
    await message.reply("Введите пароль:")

async def admin_password_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data['username']
    password = message.text
    if authenticate_admin(db_session, username, password):
        await message.reply("Доступ предоставлен.")
        
    else:
        await message.reply("Доступ запрещен.")
    await state.finish()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_command_start, commands=['admin'], state="*")
    dp.register_message_handler(admin_username_received, state=AdminLogin.waiting_for_username)
    dp.register_message_handler(admin_password_received, state=AdminLogin.waiting_for_password)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
register_handlers_admin(dp)
