from aiogram.types import Message
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.config import ADMINS_ID
from loader import dp, db
from keyboards.default import admin_start_keyboard, back_keyboard


class CreatePromocode(StatesGroup):
    get_name = State()
    get_sum = State()
    get_type = State()
    get_date = State()
    
    
promocode_type_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Одноразовый'), KeyboardButton('Закончится в определенную дату')],
        [KeyboardButton('Назад'), KeyboardButton('Главное меню')]
    ], 
    resize_keyboard=True
)
 
    
@dp.message_handler(text='Создать промокод', user_id=ADMINS_ID, state=None)
async def create_promocode_message(message: Message):
    await message.answer(
        'Введите сам промокод: ', 
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)
    )
    await CreatePromocode.get_name.set()
    
    
@dp.message_handler(user_id=ADMINS_ID, state=CreatePromocode.get_name)
async def get_promocode_name(message: Message, state: FSMContext):
    name = message.text
    
    if name == 'Назад':
        await state.finish()
        await message.answer(text='Перехожу в главное меню', reply_markup=admin_start_keyboard)
        return
    
    await state.update_data(name=name)
    await message.answer(
        text=f'Отлично, вы создали промокод {name}! Теперь введите на какую сумму он пополнит баланс:',
        reply_markup=back_keyboard
    )
    await CreatePromocode.get_sum.set()
    

@dp.message_handler(user_id=ADMINS_ID, state=CreatePromocode.get_sum)
async def get_promocode_sum(message: Message, state: FSMContext):
    sum = message.text
    data = await state.get_data()
    promocode_name = data['name']
    
    if sum.strip().isdigit():
        await state.update_data(sum=int(sum))
        await message.answer(
            text=f'Замечательно! Вы создали промокод {promocode_name} на сумму {sum} $. Теперь нужно выбрать тип этого промокода:',
            reply_markup=promocode_type_keyboard
        )
        await CreatePromocode.get_type.set()
        return
    
    elif sum == 'Назад':
        await state.reset_data()
        await message.answer(
            text='Введите сам промокод: ',
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)    
        )
        await CreatePromocode.get_name.set()
        return
        
    elif sum == 'Главное меню':
        await state.finish()
        await message.answer(
            text='Перехожу в главное меню',
            reply_markup=admin_start_keyboard
        )
        return 
    
    else:
        await message.answer(text='Я не понимаю вашего сообщения', reply_markup=back_keyboard)
        await CreatePromocode.get_sum.set()
        return 
    

@dp.message_handler(user_id=ADMINS_ID, state=CreatePromocode.get_type)
async def get_promocode_type(message: Message, state: FSMContext):
    promocode_type = message.text
    data = await state.get_data()
    
    if promocode_type == 'Одноразовый':
        await db.create_promocode(data['name'], data['sum'], True)
        await state.finish()
        await message.answer('Вы успешно зарегистрировали промокод', reply_markup=admin_start_keyboard)
        return
    
    elif promocode_type == 'Закончится в определенную дату':
        await message.answer('Через сколько дней закончится промокод? (Отправьте число)', reply_markup=back_keyboard)
        await CreatePromocode.get_date.set()
        return
    
    elif promocode_type == 'Назад':
        name = data['name']
        
        await message.answer(
            text=f'Отлично, вы создали промокод {name}! Теперь введите на какую сумму он пополнит баланс:',
            reply_markup=back_keyboard
        )
        await CreatePromocode.get_sum.set()
        return 
    
    elif promocode_type == 'Главное меню':
        await state.finish()
        await message.answer(
            text='Перехожу в главное меню',
            reply_markup=admin_start_keyboard
        )
        return 
    
    else:
        await message.answer(text='Я не понимаю вашего сообщения', reply_markup=back_keyboard)
        await CreatePromocode.get_type.set()
        return
    
    
@dp.message_handler(user_id=ADMINS_ID, state=CreatePromocode.get_date)
async def get_date_promocode(message: Message, state: FSMContext):
    days = message.text
    data = await state.get_data()
    
    if days.strip().isdigit():
        await state.finish()
        await db.create_promocode(data['name'], data['sum'], False, int(days))
        await message.answer('Вы успешно зарегистрировали промокод', reply_markup=admin_start_keyboard)
        return
    
    elif days == 'Назад':
        await message.answer('Через сколько дней закончится промокод? (Отправьте число)', reply_markup=back_keyboard)
        await CreatePromocode.get_date.set()
        return
    
    elif days == 'Главное меню':
        await state.finish()
        await message.answer(
            text='Перехожу в главное меню',
            reply_markup=admin_start_keyboard
        )
        return 
    
    else:
        await message.answer(text='Я не понимаю вашего сообщения', reply_markup=back_keyboard)
        await CreatePromocode.get_date.set()
        return
    
