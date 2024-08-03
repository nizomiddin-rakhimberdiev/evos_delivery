from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

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

geo_location = {
    "ru": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🗺 Мои адреса")],
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True), KeyboardButton(text="⬅️ Назад")]
    ]),
    "uz": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🗺 Mening manzillarim")],
        [KeyboardButton(text="📍 Geolokatsiyani yuborish", request_location=True), KeyboardButton(text="⬅️ Ortga")]
    ])
}



def create_location_buttons(locations, lang):
    my_manzil = {
        "ru": ReplyKeyboardMarkup(resize_keyboard=True, row_width=1),
        "uz": ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    }

    btns_ru = []
    btns_uz = []

    for location in locations:
        print(location[0], location)
        btns_ru.append(KeyboardButton(text=location[0]))
        btns_uz.append(KeyboardButton(text=location[0]))

    btns_ru.append(KeyboardButton(text="⬅️ Назад"))
    btns_uz.append(KeyboardButton(text="⬅️ Ortga"))

    my_manzil["ru"].add(*btns_ru)
    my_manzil["uz"].add(*btns_uz)

    return my_manzil[lang]


confirm = {
    "ru": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")],
        [KeyboardButton(text="⬅️ Назад")]
    ]),
    "uz": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="✅ Ha"), KeyboardButton(text="❌ Yo'q")],
        [KeyboardButton(text="⬅️ Ortga")]
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


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Add category"),
            KeyboardButton(text="Add product")
        ]
    ],
    resize_keyboard=True
)


async def get_categories_btn():
    categories = db.get_categories()
    categories_btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = []
    print(categories)
    for category in categories:
        btns.append(KeyboardButton(text=category[1]))
    categories_btn.add(*btns)
    return categories_btn


async def get_products_btn(category_name):
    products = db.get_products(category_name)
    products_btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    products_btn.add(KeyboardButton(text="Savat"))
    btns = []
    for product in products:
        btns.append(KeyboardButton(text=product[0]))
    products_btn.add(*btns)
    return products_btn
