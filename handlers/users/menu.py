from loader import dp, db
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.keyboards import create_location_buttons,  contact_request, back_button, menu, confirm, geo_location
from keyboards.inline.inline_keyboards import  vaqt
from states.all_states import AddLocationState, AddressState
from utils.db_api.apis import get_address_from_coordinates

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
        await call.message.answer("<b>Yetkazib berish vaqtini tanlang</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
        # await message.answer("<b>Kunduzgi menu 10:01 dan 06:30 gacha</b>", parse_mode="HTML")
        # await message.answer("Bo'limni tanlang.")
    else:
        await call.message.answer("<b>Выберите время доставки</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
        # await message.answer("<b>Меню Дневной с 10:01 до 06:30</b>", parse_mode="HTML")
        # await message.answer("Выберите категорию.")
    await AddressState.time.set()




