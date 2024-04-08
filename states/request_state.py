from aiogram.fsm.state import State, StatesGroup


class KnowledgeRequestState(StatesGroup):
    waiting_for_request_content = State()

class EditRequestState(StatesGroup):  # is it necessary really?
    waiting_for_request_content = State()
