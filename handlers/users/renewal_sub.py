from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from loader import dp
from keyboards.default import sub_time_keyboard, sub_menu_keyboard, no_money_keyboard
from texts import renewal_sub_text, back_to_menu_text, unocorrect_text, unsuccessful_sub_text
from states import RenewalSub
from utils import buy_subscribe, get_sub_type


@dp.message_handler(text='💶 Продлить подписку', state=None)
async def send_types(message: Message):
    await RenewalSub.get_time.set()
    await message.answer(text=renewal_sub_text, reply_markup=sub_time_keyboard)
    

@dp.message_handler(state=RenewalSub.get_time)
async def get_time_sub(message: Message, state: FSMContext):
    time = message.text 
    user_id = message.from_user.id
    
    try:
        months, price = await get_sub_type(time)
    except (ValueError, TypeError):
        if time == 'Назад':
            await message.answer(text=back_to_menu_text, reply_markup=sub_menu_keyboard)
            await state.reset_state()
            return
        else:
            await message.answer(text=unocorrect_text, reply_markup=sub_time_keyboard)
            await RenewalSub.get_sub_type.set()
            return
    else:        
        is_successful = await buy_subscribe(user_id, price, months)
        
        await state.reset_data()
        await state.reset_state()
        
        if is_successful:
            await message.answer(text='Вы успешно продлили подписку', reply_markup=sub_menu_keyboard)
        else:
            await message.answer(text=unsuccessful_sub_text, reply_markup=no_money_keyboard)