from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_keyboard():
    buttons = [
        [KeyboardButton(text="Новый запрос")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
