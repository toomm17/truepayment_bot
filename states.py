from aiogram.dispatcher.filters.state import State, StatesGroup


class BuySub(StatesGroup):
    get_time = State()
    get_email = State()
    
    
class RenewalSub(StatesGroup):
    get_time = State()
    update_sub = State() # Под вопросом
    
    
class UserIdea(StatesGroup):
    get_text = State()

