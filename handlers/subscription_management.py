from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from db.crud import subscribe_to_tag, subscribe_to_responses, unsubscribe
from db.database import SessionLocal

async def subscribe(message: types.Message):
    args = message.get_args().split()
    if len(args) >= 1:
        async with SessionLocal() as session:
            if args[0] == "tag" and len(args) == 2:
                tag_id = int(args[1])
                subscribe_to_tag(session, message.from_user.id, tag_id)
                await message.answer("Вы подписались на тег.")
            elif args[0] == "responses":
                subscribe_to_responses(session, message.from_user.id)
                await message.answer("Вы подписались на уведомления о ответах.")
            else:
                await message.answer("Неправильный формат команды. Используйте /subscribe tag <tag_id> или /subscribe responses")

async def unsubscribe(message: types.Message):
    args = message.get_args().split()
    if len(args) == 1 and args[0].isdigit():
        subscription_id = int(args[0])
        async with SessionLocal() as session:
            unsubscribe(session, message.from_user.id, subscription_id)
            await message.answer("Вы отписались.")
    else:
        await message.answer("Укажите корректный ID подписки для отписки.")

def register_subscription_handlers(dp: Dispatcher):
    dp.register_message_handler(subscribe, Command(commands=['subscribe']), state="*")
    dp.register_message_handler(unsubscribe, Command(commands=['unsubscribe']), state="*")
