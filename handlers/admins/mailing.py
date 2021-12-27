from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.exceptions import ChatNotFound

from data.config import ADMINS_ID
from keyboards.default import back_keyboard, admin_start_keyboard
from loader import dp, db, bot


class Mailing(StatesGroup):
    get_text = State()


@dp.message_handler(user_id=ADMINS_ID, text='Рассылка информации', state=None)
async def send_msg(message: Message):
    await message.answer(
        text='Введите сообщение рассылки:',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)
    )
    await Mailing.get_text.set()
    
    
@dp.message_handler(user_id=ADMINS_ID, state=Mailing.get_text)
async def send_text(message: Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await state.finish()
        await message.answer(text='Перехожу в главное меню', reply_markup=admin_start_keyboard)
    else:
        users_id_record = await db.get_all_id()
        users_id_list = [user['telegram_id'] for user in users_id_record]
        
        for user_id in users_id_list:
            try:
                await state.finish()
                await bot.send_message(user_id, text, reply_markup=admin_start_keyboard)
            except ChatNotFound:
                continue
    
    