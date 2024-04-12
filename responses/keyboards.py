from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from db.models import KnowledgeRequest, Response


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
        button_text = "От @{}: {}...".format(
            request.user.tg_name, request.content.split("\n")[0]
        )
        callback_data = f"request_{request.id}"
        button = InlineKeyboardButton(
            text=button_text, callback_data=callback_data)
        buttons.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_responses_keyboard(responses: List[Response]) -> InlineKeyboardMarkup:
    buttons = []
    for response in responses:
        button_text = "От @{}: {}...".format(
            response.user.tg_name, response.content.split("\n")[0]
        )
        callback_data = f"response_{response.id}"
        button = InlineKeyboardButton(
            text=button_text, callback_data=callback_data)
        buttons.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_request_actions_keyboard(request_id):
    buttons = [
        [InlineKeyboardButton(text="Добавить ответ",
                              callback_data=f"addresponse_{request_id}")],
        [InlineKeyboardButton(text="просмотреть ответы",
                              callback_data=f"viewresponse_{request_id}")],
        [InlineKeyboardButton(text="Редактировать запрос",
                                callback_data=f"editrequest_{request_id}")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_response_actions_keyboard(response_id):
    buttons = [
        [InlineKeyboardButton(text="Редактировать ответ",
                              callback_data=f"editresponse_{response_id}")],
        [InlineKeyboardButton(text="Удалить ответ",
                                callback_data=f"deleteresponse_{response_id}")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
    
    
    def get_voting_keyboard(entity_id: int, entity_type: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Голос за", callback_data=f"vote_{entity_type}_{entity_id}_1"),
         InlineKeyboardButton("Голос против", callback_data=f"vote_{entity_type}_{entity_id}_-1")]
    ])