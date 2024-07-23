from aiogram.dispatcher.filters.state import State, StatesGroup

class FeedbackState(StatesGroup):
    waiting_for_contact = State()
    waiting_for_feedback = State()


class AddLocationState(StatesGroup):
    location = State()
    confirm_location = State()
    


class AddressState(StatesGroup):
    address  = State()
    time = State()