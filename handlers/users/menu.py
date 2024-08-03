from loader import dp, db, bot
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.keyboards import create_location_buttons,  contact_request, back_button, menu, confirm, geo_location, get_categories_btn, get_products_btn
from keyboards.inline.inline_keyboards import  vaqt, get_basket_keyboard
from states.all_states import AddLocationState, AddressState
from utils.db_api.apis import get_address_from_coordinates


user_data = {}


@dp.message_handler(lambda message: message.text == "Savat", state='*')
async def get_basket(message: types.Message):
    user_id = message.from_user.id
    basket = db.get_my_basket(user_id)
    total_price = 0
    text = f""
    for b in basket:
        text += f"{b[1]} {b[0]}\n"
        total_price += b[2]

    text += f"Mahsulotlar: {total_price} so'm\n"
    text += "Yetkazib berish: 12 000 so'm\n"
    text += f"Jami: {total_price + 12000}"

    await message.answer(text)

@dp.message_handler(text="🍴 Меню")
async def geo(message: types.Message):
    await message.answer("Отправьте 📍 геолокацию или выберите адрес доставки", reply_markup=geo_location[db.check_language(message.from_user.id)])
    await AddLocationState.location.set()




@dp.message_handler(content_types=types.ContentType.LOCATION, state=AddLocationState.location)
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    chat_id = message.from_user.id

    address = await get_address_from_coordinates(latitude, longitude)

    db.add_address(chat_id, address, latitude, longitude)
    if db.check_language(message.from_user.id) == "ru":
        await message.reply(f"Адрес, по которому вы хотите заказать: {address} Вы подтверждаете этот адрес?", reply_markup=confirm[db.check_language(message.from_user.id)])
    else:
        await message.answer(f"Buyurtma bermoqchi bo'lgan manzil: {address} Ushbu manzilni tasdiqlaysizmi?", reply_markup=confirm[db.check_language(message.from_user.id)])
    await AddLocationState.confirm_location.set()


@dp.message_handler(text=["✅ Да", "✅ Ha"], state=AddLocationState.confirm_location)
async def confirm_address(message: types.Message):
    if db.check_language(message.from_user.id) == "uz":
        await message.answer("<b>Yetkazib berish vaqtini tanlang</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
        # await message.answer("<b>Kunduzgi menu 10:01 dan 06:30 gacha</b>", parse_mode="HTML")
        # await message.answer("Bo'limni tanlang.")
    else:
        await message.answer("<b>Выберите время доставки</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
        # await message.answer("<b>Меню Дневной с 10:01 до 06:30</b>", parse_mode="HTML")
        # await message.answer("Выберите категорию.")
    await AddressState.time.set()




@dp.message_handler(lambda message: message.text in ["🗺 Мои адреса", "🗺 Mening manzillarim"], state="*")
async def adresa(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.from_user.id
    locations = db.get_addresses(chat_id)

    lang = db.check_language(message.from_user.id)

    reply_markup = create_location_buttons(locations, lang)

    if lang == "ru":
        await message.answer("Выберите адрес доставки", reply_markup=reply_markup)
    else:
        await message.answer("Yetkazib berish manzilni tanlang", reply_markup=reply_markup)
    await AddressState.address.set()


@dp.message_handler(state=AddressState.address)
async def set_address(message: types.Message, state:FSMContext):
    address = message.text
    chat_id = message.from_user.id
    await state.update_data(address=address, chat_id=chat_id)
    if db.check_language(message.from_user.id) == "uz":
        await message.answer("<b>Yetkazib berish vaqtini tanlang</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
        # await message.answer("<b>Kunduzgi menu 10:01 dan 06:30 gacha</b>", parse_mode="HTML")
        # await message.answer("Bo'limni tanlang.")
    else:
        await message.answer("<b>Выберите время доставки</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
        # await message.answer("<b>Меню Дневной с 10:01 до 06:30</b>", parse_mode="HTML")
        # await message.answer("Выберите категорию.")
    await AddressState.time.set()


@dp.callback_query_handler(lambda c: c.data.startswith("now"), state=AddressState.time)
async def set_time(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split('_')[1]
    chat_id = call.from_user.id
    time = datetime.datetime.now()
    await state.update_data(time=time)
    if db.check_language(call.message.from_user.id) == "uz":
        await call.message.answer("<b>Kategoriyalardan birini tanlang</b>", parse_mode="HTML", reply_markup=await get_categories_btn())
        # await message.answer("<b>Kunduzgi menu 10:01 dan 06:30 gacha</b>", parse_mode="HTML")
        # await message.answer("Bo'limni tanlang.")
    else:
        await call.message.answer("<b>Выберите время доставки</b>", parse_mode="HTML", reply_markup=await get_categories_btn())
        # await message.answer("<b>Меню Дневной с 10:01 до 06:30</b>", parse_mode="HTML")
        # await message.answer("Выберите категорию.")
    await AddressState.category.set()



@dp.message_handler(state=AddressState.category)
async def set_category(message: types.Message, state: FSMContext):
    category_name = message.text
    await message.answer("Productlardan birini tanlang: ", reply_markup=await get_products_btn(category_name))
    await AddressState.product.set()


@dp.message_handler(state=AddressState.product)
async def get_products_handler(message: types.Message, state: FSMContext):
    product_name = message.text
    data = db.get_product(product_name)
    image = data[0][4]
    description = data[0][3]
    price = data[0][2]
    caption = f"{description}\n\nNarxi: {price} 000"

    product_id = data[0][0]
    count = user_data.get(message.from_user.id, {}).get(product_id, 1)

    keyboard = await get_basket_keyboard(product_id, count)
    await message.answer_photo(photo=image, caption=caption, reply_markup=keyboard)
    
    


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('increment', 'decrement', 'add_to_cart')), state='*')
async def process_callback(callback_query: types.CallbackQuery):
    action, product_id = callback_query.data.split(':')
    user_id = callback_query.from_user.id
    print(user_id, 'knopkani bosdi')
    if user_id not in user_data:
        user_data[user_id] = {}
    if product_id not in user_data[user_id]:
        user_data[user_id][product_id] = 1
    
    if action == 'increment':
        user_data[user_id][product_id] += 1
    elif action == 'decrement' and user_data[user_id][product_id] > 1:
        user_data[user_id][product_id] -= 1
    elif action == 'add_to_cart':
        product_name = db.get_product_name(product_id)
        price = db.get_product_price(product_id)
        count = user_data[user_id][product_id]
        total_price = int(price) * count * 1000
        db.add_basket(user_id, product_name, count, total_price)
        await bot.send_message(
            callback_query.from_user.id,
            f"{product_name} ({count} x {price} so'm) savatchaga qo'shildi. Jami: {total_price} so'm"
        )
        return
    
    count = user_data[user_id][product_id]
    keyboard = await get_basket_keyboard(product_id, count)
    await bot.edit_message_reply_markup(
        callback_query.message.chat.id, 
        callback_query.message.message_id, 
        reply_markup=keyboard
    )
    await bot.answer_callback_query(callback_query.id)




    