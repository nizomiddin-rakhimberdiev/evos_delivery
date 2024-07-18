from aiogram.dispatcher.filters.state import State, StatesGroup

class FeedbackState(StatesGroup):
    waiting_for_contact = State()
    waiting_for_feedback = State()