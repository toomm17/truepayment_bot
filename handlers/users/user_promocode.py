from datetime import datetime, date

from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
from handlers.admins.promocode import get_promocode_name

from loader import db, dp
from utils import get_keyboard


class ActivatePromocode(StatesGroup):
    get_promocode_name = State()


@dp.message_handler(text='🔢 Ввести промокод', state=None)
async def send_promocode_info(message: Message, state: FSMContext):
    await message.answer(
        text='Мы постарались и сделали для вас систему промокодов.\nТут вы можете ввести свой промокод и ваш баланс пополнится:',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)
    )
    await ActivatePromocode.get_promocode_name.set()
    return 


@dp.message_handler(state=ActivatePromocode.get_promocode_name)
async def check_promocode(message: Message, state: FSMContext):
    promocode = message.text
    user_id = message.from_user.id
    
    if promocode == 'Назад':
        await state.finish()
        await message.answer(
            'Перехожу в главное меню',
            reply_markup = await get_keyboard(user_id)
        )
        return
    
    is_promo = await db.get_promocode(promocode)
    
    if is_promo:
        # Промокод используется один раз
        
        user_promocodes = await db.get_user_promocode(user_id)
        
        if user_promocodes.get('promocode'):
            await state.finish()
            await message.answer(text='Вы не можете активировать больше одного промокода', reply_markup=await get_keyboard(user_id))
            return
         
        if is_promo.get('is_disposable'):
            await db.deactivate_promocode(promocode)
            await db.user_update_promocode(user_id, promocode)
            promocode_sum = is_promo.get('sum')
            await db.update_balance(user_id, promocode_sum, 'plus')
            await message.answer(
                text=f'Вы успешно активировали промокод.\nВаш баланс пополнен на {promocode_sum} $.',
                reply_markup=await get_keyboard(user_id)
            )
            await state.finish()
            return
        
        else:
            user_poromocodes = await db.get_user_promocode(user_id)    
            
            if user_poromocodes.get('promocode'):
                await state.finish()
                
                if promocode in list(user_poromocodes.get('promocode')):
                    text = 'Вы уже использовали этот промокод..',
                else:
                    text = 'Вы не можете активировать больше одного промокода'
                
                await message.answer(text=text, reply_markup=await get_keyboard(user_id))
                return 
            
            else:        
                promocode_end_date = is_promo.get('end_date')
                
                if date.today() <= promocode_end_date:
                    await db.user_update_promocode(user_id, promocode)
                    promocode_sum = is_promo.get('sum')
                    await db.update_balance(user_id, promocode_sum, 'plus')
                    await message.answer(
                        text=f'Вы успешно активировали промокод.\nВаш баланс пополнен на {promocode_sum} $.',
                        reply_markup=await get_keyboard(user_id)
                    )
                    await state.finish()
                    return
   
    await message.answer(
        text='Этого промокода нет или он уже недействителен',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)
    )
    await ActivatePromocode.get_promocode_name.set()
                
            
            
    
    

   
    


