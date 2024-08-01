from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

vaqt = {
    'uz': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Hozir", callback_data='now_uz'), InlineKeyboardButton(text="Boshqa vaqtda", callback_data='other_uz')]
    ]),
    'ru': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сейчас", callback_data='now_ru'), InlineKeyboardButton(text="В другое время", callback_data='now_ru')]
    ])
}




async def get_catedories_btn():
    categories = db.get_categories()
    categories_btn = InlineKeyboardMarkup(row_width=2)
    btns = []
    print(categories)
    for category in categories:
        btns.append(InlineKeyboardButton(text=category[1], callback_data=f"category_{category[0]}"))
    categories_btn.add(*btns)
    return categories_btn


async def get_basket_keyboard(product_id, count):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("-", callback_data=f"decrement:{product_id}"),
        InlineKeyboardButton(f"{count}", callback_data=f"count:{product_id}"),
        InlineKeyboardButton("+", callback_data=f"increment:{product_id}")
    )
    keyboard.add(
        InlineKeyboardButton("Savatga qo'shish", callback_data=f"add_to_cart:{product_id}")
    )
    return keyboard