from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_keyboard():
    buttons = [
        [KeyboardButton(text="Новый запрос")],
        [KeyboardButton(text="Просмотреть запросы")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
