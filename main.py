import logging

from aiogram import Bot, Dispatcher, executor, types

with open("bot.token", encoding="UTF-8") as f:
    TOKEN=f.read()
API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text[::-1])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)