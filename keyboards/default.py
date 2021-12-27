from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('💰 Пополнить баланс'), KeyboardButton('💶 Оплатить подписку')],
        [KeyboardButton('👤 Личный кабинет'), KeyboardButton('💌 Оставить отзыв')],
        [KeyboardButton('🆘 Получить помощь'), KeyboardButton('🤔 Предложить идею поста')],
        [KeyboardButton('🔢 Ввести промокод')]
    ],
    resize_keyboard=True
)

sub_menu_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('💰 Пополнить баланс'), KeyboardButton('💶 Продлить подписку')],
        [KeyboardButton('👤 Личный кабинет'), KeyboardButton('💌 Оставить отзыв')],
        [KeyboardButton('🆘 Получить помощь'), KeyboardButton('🤔 Предложить идею поста')],
        [KeyboardButton('🔢 Ввести промокод')]
    ],
    resize_keyboard=True
)

personal_area_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('💰 Пополнить баланс'), KeyboardButton('💶 Оплатить подписку')],
        [KeyboardButton('Главное меню')]
    ],
    resize_keyboard=True
)

pa_subs_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('💰 Пополнить баланс'), KeyboardButton('💶 Продлить подписку')],
        [KeyboardButton('Главное меню')]
    ],
    resize_keyboard=True
)

sub_time_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('1 месяц - 39$'), KeyboardButton('3 месяца - 109$ (7% скидка)')],
        [KeyboardButton('6 месяцев - 209$ (10% скидка)'), KeyboardButton('12 месяцев - 399$ (15% скидка)')],
        [KeyboardButton('Назад')]
    ],
    resize_keyboard=True
)

back_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Назад'), KeyboardButton('Главное меню')]
    ], 
    resize_keyboard=True
)

no_money_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('💰 Пополнить баланс'), KeyboardButton('Главное меню')],
    ],
    resize_keyboard=True
)

admin_start_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Выгрузить почты в .csv'), KeyboardButton('Накрутить баланс')],
        [KeyboardButton('Рассылка информации'), KeyboardButton('Проверка подписки')],
        [KeyboardButton('Создать промокод')]
    ]
)
