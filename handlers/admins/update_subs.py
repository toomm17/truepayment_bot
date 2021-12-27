from datetime import datetime
from dateutil.relativedelta import relativedelta

from aiogram.types import Message

from data.config import ADMINS_ID
from loader import dp, db, bot
from keyboards.default import admin_start_keyboard


async def diff_dates(end_sub):
    now = datetime.today().strftime('%Y-%m-%d')
    send_msg_date = end_sub - relativedelta(days=3)
    return now == send_msg_date.strftime('%Y-%m-%d')


@dp.message_handler(user_id=ADMINS_ID, text='Проверка подписки')
async def check_subs(message: Message):
    # Подумать над лучшей реализацией
    users_id_record = await db.get_all_id()
    users_id_list = [user['telegram_id'] for user in users_id_record]
    
    end_sub_users = []
    
    for user_id in users_id_list:
        user_data = await db.get_all_info(telegram_id=user_id)
        end_sub = user_data['end_sub']
        
        if end_sub:
            is_send_date = await diff_dates(end_sub)
            
            if is_send_date:
                await bot.send_message(user_id, 'Ваша подписка скоро закончится!!1')
                end_sub_users.append(user_id)
                
    await message.answer(
        text=f'Проверка успешно выполнена.\nПодписка скоро закончится у {len(end_sub_users)} человек.',
        reply_markup=admin_start_keyboard
    )