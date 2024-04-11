# for now, copypasted from view_requests.py
from aiogram import types, Router, F
import logging

from responses.response_messages import RESPONSE_MESSAGES
from responses.keyboards import get_start_keyboard, get_responses_keyboard, get_response_actions_keyboard

from db import crud
from db.database import get_db

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

view_responses_router = Router()

@view_responses_router.callback_query(F.data.startswith("viewresponse_"))
async def view_responses(callback: types.CallbackQuery):
    request_id = int(callback.data.split("_")[1])
    try:
        with get_db() as db:
            responses = crud.get_responses_for_request(db, request_id)
            if not responses:
                await callback.message.answer(RESPONSE_MESSAGES["no_responses_message"], reply_markup=get_start_keyboard())
                return

            keyboard = get_responses_keyboard(responses)
            await callback.message.answer(RESPONSE_MESSAGES["view_responses_prompt"], reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error viewing responses: {e}")
        await callback.message.answer(RESPONSE_MESSAGES["error_message"])

@view_responses_router.callback_query(F.data.startswith("response_"))
async def view_response(callback: types.CallbackQuery):
    response_id = int(callback.data.split("_")[1])
    try:
        with get_db() as db:
            response = crud.get_response(db, response_id)
            if response:
                await callback.message.answer(response.content, reply_markup=get_response_actions_keyboard(response_id))
            else:
                await callback.message.answer(RESPONSE_MESSAGES["response_not_found"])
    except Exception as e:
        logger.error(f"Error viewing a specific response: {e}")
        await callback.message.answer(RESPONSE_MESSAGES["error_message"])
