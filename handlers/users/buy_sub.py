import re
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from keyboards.default import (
    sub_time_keyboard, menu_keyboard, back_keyboard, sub_menu_keyboard,
    no_money_keyboard
)
from loader import dp, bot
from states import BuySub
from texts import (
    buy_sub_text, unocorrect_text, back_to_menu_text, send_email_text, successful_sub_text,
    unsuccessful_sub_text, uncorrect_email_text
)
from utils import get_sub_type, buy_subscribe, gen_chat_link, post_req


@dp.message_handler(text='💶 Оплатить подписку', state=None)
async def send_time_sub(message: Message):
    await BuySub.get_time.set()
    return await message.answer(text=buy_sub_text, reply_markup=sub_time_keyboard)


@dp.message_handler(state=BuySub.get_time)
async def get_time_sub(message: Message, state: FSMContext):
    time = message.text
    
    try:
        months, price = await get_sub_type(time)
    except (ValueError, TypeError):
        if time == 'Назад':
            await message.answer(text=back_to_menu_text, reply_markup=menu_keyboard)
            await state.finish()
            return
        else:
            await message.answer(text=unocorrect_text, reply_markup=sub_time_keyboard)
            await BuySub.get_time.set()
            return
    else:        
        await state.update_data(price=price, count_months=months)    
        await BuySub.get_email.set()
        return await message.answer(text=send_email_text, reply_markup=back_keyboard)
        

@dp.message_handler(state=BuySub.get_email)
async def get_sub_email(message: Message, state: FSMContext):
    email = message.text
    user_id = message.from_user.id
    
    data = await state.get_data()
    price = data['price']
    months = data['count_months']
    
    pattern = r'^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$'
    
    if re.match(pattern, email) is not None:
        is_successful = await buy_subscribe(user_id, price, months, email)
        await state.reset_data()
        await state.finish()
        
        if is_successful:
            invite_link = await gen_chat_link()
            status_code = await post_req(email)
            print(status_code)
            await message.answer(text=successful_sub_text.format(invite_link), reply_markup=sub_menu_keyboard)
            await bot.send_message(609806289, text=f'Подписался {email}')
        else:
            await message.answer(text=unsuccessful_sub_text, reply_markup=no_money_keyboard)        
    
    elif email == 'Назад':
        await BuySub.get_time.set()
        await message.answer(text=buy_sub_text, reply_markup=sub_time_keyboard)

    elif email == 'Главное меню':
        await state.reset_data()
        await state.reset_state()
        await message.answer(text=back_to_menu_text, reply_markup=menu_keyboard)
    
    else:
        await BuySub.get_email.set()
        await message.answer(text=uncorrect_email_text, reply_markup=back_keyboard)
