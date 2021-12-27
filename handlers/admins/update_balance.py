from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.config import ADMINS_ID
from keyboards.default import back_keyboard, admin_start_keyboard
from loader import dp, db



class UpBalance(StatesGroup):
    get_user_id = State()
    get_new_balance = State()


@dp.message_handler(user_id=ADMINS_ID, text='Накрутить баланс', state=None)
async def balance_upp(message: Message):
    await message.answer(
        text='Для пополнения баланса нужно отправить id пользователя.',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)
    )
    await UpBalance.get_user_id.set()
    
    
@dp.message_handler(user_id=ADMINS_ID, state=UpBalance.get_user_id)
async def get_id(message: Message, state: FSMContext):
    id = message.text
    
    if id.isdigit():
        await state.update_data(id=int(id))
        await message.answer(
            text='На какое количество долларов пополнить баланс?',
            reply_markup=back_keyboard
        )
        await UpBalance.get_new_balance.set()
    
    elif message.text == 'Назад':
        await state.finish()
        await message.answer(
            text='Перехожу в главное меню', 
            reply_markup=admin_start_keyboard
        )    
        
    else:
        await message.answer(
            text='id пользователя должен состоять только из цифр',
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)
        )
        await UpBalance.get_user_id.set()
        
        
@dp.message_handler(user_id=ADMINS_ID, state=UpBalance.get_new_balance)
async def up_balance(message: Message, state: FSMContext):
    new_balance = message.text
    data = await state.get_data()
    id = data['id']
    
    if new_balance.isdigit():
        await db.update_balance(id, int(new_balance), 'plus')
        await state.finish()
        await message.answer(
            text='Баланс пользователя успешно пополнен',
            reply_markup=admin_start_keyboard
        )
        
    elif new_balance == 'Назад':
        await state.reset_data()
        await message.answer(
            text='Для пополнения баланса нужно отправить id пользователя.',
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)    
        )
        await UpBalance.get_user_id.set()
    
    elif new_balance == 'Главное меню':
        await state.finish()
        await message.answer(
            text='Перехожу в главное меню',
            reply_markup=admin_start_keyboard
        )
    
    else:
        await message.answer(
            text='Баланс должен состоять из чисел',
            reply_markup=back_keyboard
        )
        await UpBalance.get_new_balance.set()

    
