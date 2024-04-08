from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_keyboard():
    buttons = [
        [KeyboardButton(text="Новый запрос")]
        [KeyboardButton(text="Просмотреть запросы")]  # not here I think.
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
