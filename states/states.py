from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    waiting_for_request_content = State()
    waiting_for_response_content = State()
    waiting_for_edited_content = State()
