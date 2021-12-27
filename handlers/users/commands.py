from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import CommandStart, Command, ChatTypeFilter
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

from asyncpg.exceptions import UniqueViolationError

from data.config import ADMINS_ID, PRIVATE_CHANNEL_ID, OFFERS_CHANNEL_ID
from keyboards.default import menu_keyboard, admin_start_keyboard
from loader import dp, db, bot
from texts import (
    unique_start_text, db_user_start_text, feedback_text, help_text, balance_rep_text,
    offers_text, personal_area, back_to_menu_text
)
from keyboards.inline import feedback_keyboard, help_keyboard, token_keyboard
from utils import get_keyboard
from states import UserIdea


@dp.message_handler(ChatTypeFilter(chat_type=ChatType.SUPERGROUP))
async def send_kick_msg(message: Message):
    pass


@dp.message_handler(CommandStart(), ChatTypeFilter(chat_type=ChatType.PRIVATE), user_id=ADMINS_ID)
async def admin_start(message: Message):
    await message.answer(text='Привет, хозяин.', reply_markup=admin_start_keyboard)


@dp.message_handler(CommandStart(), ChatTypeFilter(chat_type=ChatType.PRIVATE))
async def bot_start(message: Message):
    name = message.from_user.username if message.from_user.first_name is None else message.from_user.first_name
    user_id = message.from_user.id
    await db.create_table_users()
    try:
        await db.add_user(name, user_id)
        text = unique_start_text
        keyboard = menu_keyboard
    except UniqueViolationError:
        text = db_user_start_text
        keyboard = await get_keyboard(user_id)

    return await message.answer(text=text, reply_markup=keyboard)


@dp.message_handler(text='💌 Оставить отзыв')
async def send_feedback(message: Message):
    return await message.answer(text=feedback_text, reply_markup=feedback_keyboard)


@dp.message_handler(text='🆘 Получить помощь')
async def get_help(message: Message):
    return await message.answer(text=help_text, reply_markup=help_keyboard)


@dp.message_handler(text='Главное меню')
async def send_menu(message: Message):
    keyboard = await get_keyboard(message.from_user.id)
    return await message.answer(text='Перехожу в главное меню', reply_markup=keyboard)


@dp.message_handler(text='💰 Пополнить баланс')
async def send_tokens(message: Message):
    return await message.answer(text=balance_rep_text, reply_markup=token_keyboard)


@dp.message_handler(text='🤔 Предложить идею поста', state=None)
async def check_offer(message: Message):
    await UserIdea.get_text.set()
    back = ReplyKeyboardMarkup([[KeyboardButton('Назад')]], resize_keyboard=True)
    return await message.answer(text=offers_text, reply_markup=back)


@dp.message_handler(state=UserIdea.get_text)
async def resend_text(message: Message, state: FSMContext):
    text = message.text
    keyboard = await get_keyboard(message.from_user.id)
    if text == 'Назад':
        await state.finish()
        return await message.answer(text=back_to_menu_text, reply_markup=keyboard)
    await state.finish()
    await bot.send_message(chat_id=OFFERS_CHANNEL_ID, text=text)
    return await message.answer(text='Спасибо! Ваше предложение отправлено команде проекта.', reply_markup=keyboard)


@dp.message_handler(text='👤 Личный кабинет')
async def send_user_info(message: Message):
    tg_id = message.from_user.id
    keyboard = await get_keyboard(tg_id, True)
    info = await db.get_all_info(telegram_id=tg_id)
    balance = info['balance']
    start_sub = info['start_sub'] if not info['start_sub'] is None else 'Отсутствует'
    end_sub = info['end_sub'] if not info['end_sub'] is None else 'Отсутствует'
    email = info['email'] if not info['email'] is None else 'Отсутствует'

    return await message.answer(
        text=personal_area.format(balance, start_sub, end_sub, email),
        reply_markup=keyboard
    )
