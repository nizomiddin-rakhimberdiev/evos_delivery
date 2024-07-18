from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = {
    'ru': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='🍴 Меню')],
        [KeyboardButton(text='🛍 Мои заказы')],
        [KeyboardButton(text='✍️ Оставить отзыв'), KeyboardButton(text='⚙️ Настройки')],
    ]),
    'uzb': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='🍴 Menyu')],
        [KeyboardButton(text='🛍 Mening buyurtmalarim')],
        [KeyboardButton(text='⚙️ Sozlamalar')],
    ])
}

contact_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text="📞 Мой номер", request_contact=True)],
    [KeyboardButton(text="⬅️ Назад")]
])

back_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text="⬅️ Назад")]
])


settings_menu_btn = {
    'ru': ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Изменить язык')],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    ),
    'uzb': ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Tilni o'zgartirish")],
            [KeyboardButton(text="⬅️ Ortga")]
        ],
        resize_keyboard=True
    )
}

language_btn = {
    'ru': ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O'zbekcha")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    ),
    'uzb': ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O'zbekcha")],
            [KeyboardButton(text="⬅️ Ortga")]
        ],
        resize_keyboard=True
    )
}
