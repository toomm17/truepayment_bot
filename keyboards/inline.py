from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


token_callback = CallbackData('token', 'token_name')

payment_callback = CallbackData('payment', 'type', 'back')

token_keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='BUSD', callback_data=token_callback.new(token_name='BUSD')),
            InlineKeyboardButton(text='USDT', callback_data=token_callback.new(token_name='USDT')),
            
        ]
    ]   
)

payment_keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Binance (внутренний платеж)', callback_data=payment_callback.new(type='internal', back='None')),
            InlineKeyboardButton(text='Другое (внешний платеж)', callback_data=payment_callback.new(type='external', back='None')),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=payment_callback.new(type='None', back='True'))
        ]
    ]
)

back_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back')
        ]
    ]
)

feedback_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Написать отзыв', url='https://vk.com/topic-208291464_48134655')]
    ]
)

help_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Написать в тех.поддержку', url='https://t.me/TrueCrypto_Support')]
    ]
)
