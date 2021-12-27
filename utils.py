import aiohttp

from asyncio import sleep
from datetime import datetime
from typing import Optional, Union
from math import trunc

import aiogram.utils.exceptions
from aiogram.types import BotCommand, ReplyKeyboardMarkup, Message

from data.config import PRIVATE_CHANNEL_ID, ADMINS_ID, SITE_TOKEN
from keyboards.default import menu_keyboard, sub_menu_keyboard, pa_subs_keyboard, personal_area_keyboard
from loader import db, client, bot
from texts import have_trans_code, success_code, code_not_found, no_trans_code


async def get_keyboard(tg_id: int, is_pa: bool = False) -> ReplyKeyboardMarkup:
    is_sub_record = await db.user_is_sub(tg_id)
    is_sub = is_sub_record.get('is_sub')
    if is_pa:
        return pa_subs_keyboard if is_sub else personal_area_keyboard
    return sub_menu_keyboard if is_sub else menu_keyboard
    

async def get_amount(transaction: str, payment: str):
    response = await client.get_deposit_history()
    print(transaction)
    transaction = transaction \
        if payment == 'external' else f'Internal transfer {transaction}'
    print(transaction)
    for deposit in response:
        code = deposit['txId']
        print(code)
        if code == transaction:
            print(deposit['amount'])
            return deposit['amount']
        
        
async def up_balance(message: Message, tpayment: str):
    code = message.text
    is_unique = await db.check_transaction(code)
    if is_unique.split()[-1] != '0':
        return await message.answer(text=have_trans_code)
    else:
        for _ in range(5):
            amount = await get_amount(code, tpayment)
            
            if amount:
                amount = float(amount) if amount.find('.') != -1 else int(amount)
                if isinstance(amount, float):
                    amount = trunc(amount)
                print(amount, 'up_balance')
                await db.update_balance(int(message.from_user.id), amount, 'plus')
                await db.update_transaction(int(message.from_user.id), code)
                return await message.answer(text=success_code.format(amount))
            else:
                await message.answer(text=no_trans_code)
                await sleep(30) 
        else:
            return await message.answer(text=code_not_found)


async def get_sub_type(time: str) -> Optional[Union[str, tuple]]:        
    sub_type_dict = {
        '1 месяц - 39$': (1, 39),
        '3 месяца - 109$ (7% скидка)': (3, 109),
        '6 месяцев - 209$ (10% скидка)': (6, 209),
        '12 месяцев - 399$ (15% скидка)': (12, 399),
    }        
    return 'Назад' if time == 'Назад' else sub_type_dict.get(time, None)


async def buy_subscribe(
    user_id: int,
    price: int,
    months: int,
    email: str = None,   
) -> bool:
    user_dict = await db.get_all_info(telegram_id=user_id)
    balance = user_dict['balance']
    is_sub = user_dict['is_sub']

    if balance >= price:
        
        if is_sub:
            await db.update_balance(user_id, price, 'minus')
            await db.extend_sub(user_id, months)
            return True                
        else:
            await db.update_balance(user_id, price, 'minus')
            await db.update_sub(user_id)
            await db.update_date_sub(user_id, months)
            await db.update_email(user_id, email)
            return True
   
    else:
        return False
            
            
async def gen_chat_link() -> str:
    chat = await bot.get_chat(PRIVATE_CHANNEL_ID)
    invite_link_dict = await chat.create_invite_link(member_limit=1)
    return invite_link_dict['invite_link']


async def kick_from_channel():
    users_id_record = await db.get_all_id()
    users_id_list = [user['telegram_id'] for user in users_id_record]
    
    kick_users = []
    
    for user_id in users_id_list:
        user_data = await db.get_all_info(telegram_id=user_id)
        end_sub = user_data['end_sub']
        print(end_sub)

        if end_sub:
 
            if datetime.today().strftime('%Y-%m-%d') == end_sub.strftime('%Y-%m-%d'):
                await bot.kick_chat_member(PRIVATE_CHANNEL_ID, user_id) # CantRestrictChatOwner
                await bot.unban_chat_member(PRIVATE_CHANNEL_ID, user_id)
                await db.clear_info(user_id)
                kick_users.append(user_id)
   
    print(kick_users)
    for admin_id in ADMINS_ID:
        try:
            await bot.send_message(admin_id, text=f'Закончилась подписка у {len(kick_users)} человек/человека')
        except aiogram.utils.exceptions.ChatNotFound:
            pass
           

async def post_req(email: str) -> None:
    headers = {'Authorization': f'Token {SITE_TOKEN}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post('https://truecrypto.ru/account/api/', json={'email': email}) as resp:
            print(resp.status)
            return resp.status
            
