from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from db.models import KnowledgeRequest


def get_start_keyboard():
    buttons = [
        [KeyboardButton(text="Новый запрос")],
        [KeyboardButton(text="Просмотреть запросы")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def get_requests_keyboard(requests: List[KnowledgeRequest]) -> InlineKeyboardMarkup:
    buttons = []
    for request in requests:
        button_text = f"От @{request.user.tg_name}: {request.content[:40]}..."
        callback_data = f"request_{request.id}"
        button = InlineKeyboardButton(
            text=button_text, callback_data=callback_data)
        buttons.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_request_actions_keyboard(request_id):
    buttons = [
        [InlineKeyboardButton(text="Добавить ответ",
                              callback_data=f"add_response_{request_id}")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
