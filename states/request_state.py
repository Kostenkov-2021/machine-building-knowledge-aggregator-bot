from aiogram.fsm.state import State, StatesGroup


class KnowledgeRequestState(StatesGroup):
    waiting_for_request_content = State()
