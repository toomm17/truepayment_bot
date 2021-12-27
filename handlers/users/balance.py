from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from loader import dp, db
from middleware import rate_limit
from keyboards.inline import token_callback, payment_callback, back_keyboard, payment_keyboard, token_keyboard
from texts import (
    busd_text, usdt_text, busd_internal_text, busd_external_text, usdt_internal_text, usdt_external_text,
    balance_rep_text, uncorrect_trans_code
)
from utils import up_balance


            
@dp.callback_query_handler(token_callback.filter(token_name=['BUSD', 'USDT']))
async def send_token_info(call: CallbackQuery):
    token = call['data'].split(':')[-1]
    text = busd_text if token == 'BUSD' else usdt_text
    return await call.message.edit_text(text=text, reply_markup=payment_keyboard)
    
    
@dp.callback_query_handler(payment_callback.filter(type=['internal', 'external']))
async def send_payment_info(call: CallbackQuery):    
    token = 'BUSD' if call['message']['text'] == busd_text else 'USDT'
    payment_type = call['data'].split(':')[1]
    if token == 'BUSD':
        text = busd_internal_text if payment_type == 'internal' else busd_external_text
    else:
        text = usdt_internal_text if payment_type == 'internal' else usdt_external_text
    
    return await call.message.edit_text(text=text, reply_markup=back_keyboard, disable_web_page_preview=True)
    
    
@dp.callback_query_handler(payment_callback.filter(back='True'))
async def step_back(call: CallbackQuery):
    return await call.message.edit_text(text=balance_rep_text, reply_markup=token_keyboard)
    
    
@dp.callback_query_handler(text='back')
async def back_to_select_payment(call: CallbackQuery):
    text = call['message']['text']
    token_text = busd_text if text.find('USDT') == -1 else usdt_text
    return await call.message.edit_text(text=token_text, reply_markup=payment_keyboard)


@dp.message_handler(lambda message: message.text.isdigit())
@rate_limit(60)
async def internal_payment(message: Message):
    code = message.text
    if len(code) in (9, 10, 11, 12, 13):
        return await up_balance(message, 'internal')
    else:
        return await message.answer(text=uncorrect_trans_code)
   
    
@dp.message_handler(lambda message: len(message.text) in (62, 63, 64, 65, 66, 67, 68))
@rate_limit(60)
async def external_payment(message: Message):
    code = message.text
    if code.find(' ') == -1:
        return await up_balance(message, 'external')
    else:
        return await message.answer(text=uncorrect_trans_code)       
