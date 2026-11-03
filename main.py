import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, ADMIN_ID
from database import init_db, DB_PATH
from keyboards import (get_main_menu_kb, get_my_profile_kb, get_new_user_kb,
                       get_districts_kb, get_subcultures_kb, get_gender_kb,
                       get_looking_for_kb, get_confirm_kb)
from states import Registration

bot = Bot(token="9168726092:AAFiZen2ib0q7aWldD_MVJT8cX2f1H7ISoc")
dp = Dispatcher()

# ================= ГЛАВНОЕ МЕНЮ =================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET username = ?, last_seen = CURRENT_TIMESTAMP WHERE user_id = ?",
                         (message.from_user.username, message.from_user.id))
        await db.commit()
        async with db.execute("SELECT is_approved, is_banned FROM users WHERE user_id = ?", (message.from_user.id,)) as cursor:
            row = await cursor.fetchone()

    if row is None:
        await message.answer(f"Привет, {message.from_user.first_name}!\n\n"
                             "Это <b>Свои Люди Братск | Знакомства 🖤</b>\n\n"
                             "Здесь ты можешь найти своих людей.\nНажми кнопку ниже, чтобы создать анкету.",
                             parse_mode="HTML", reply_markup=get_new_user_kb())
        return

    is_approved, is_banned = row
    if is_banned:
        await message.answer("🚫 Ты забанен.", parse_mode="HTML")
    elif not is_approved:
        await message.answer("⏳ Твоя анкета на проверке.", parse_mode="HTML")
    else:
        await show_main_menu(message)

async def show_main_menu(message: Message):
    await message.answer("Подождем пока кто-то увидит твою анкету...\n\n"
                         "1. Смотреть анкеты.\n2. Моя анкета.\n3. Я больше не хочу никого искать.\n***\n"
                         "4. Поднять в топ 🚀", reply_markup=get_main_menu_kb())

# ================= РЕГИСТРАЦИЯ (FSM) =================
@dp.message(F.text == "📝 Создать анкету")
async def start_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отлично! Давай создадим анкету.\n\nКак тебя зовут?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.name)

@dp.message(Registration.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет? (Напиши числом)")
    await state.set_state(Registration.age)

@dp.message(Registration.age)
async def reg_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напиши возраст числом (например, 18).")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Выбери свой район:", reply_markup=get_districts_kb())
    await state.set_state(Registration.district)

# Выбор района (1 уровень - группа)
@dp.callback_query(Registration.district, F.data.startswith("dist_group_"))
async def reg_district_group(callback: CallbackQuery):
    group = callback.data.replace("dist_group_", "")
    if group == "central":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Центральный", callback_data="district_Центральный")],
            [InlineKeyboardButton(text="Бикей", callback_data="district_Бикей")],
            [InlineKeyboardButton(text="Порожский", callback_data="district_Порожский")],
            [InlineKeyboardButton(text="Сосновый", callback_data="district_Сосновый")],
            [InlineKeyboardButton(text="Стениха", callback_data="district_Стениха")],
            [InlineKeyboardButton(text="Чекановский", callback_data="district_Чекановский")]
        ])
    elif group == "right":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Гидростроитель", callback_data="district_Гидростроитель")],
            [InlineKeyboardButton(text="Осиновка", callback_data="district_Осиновка")],
            [InlineKeyboardButton(text="Сухой", callback_data="district_Сухой")]
        ])
    elif group == "padun":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Падун", callback_data="district_Падун")],
            [InlineKeyboardButton(text="Энергетик", callback_data="district_Энергетик")],
            [InlineKeyboardButton(text="Южный Падун", callback_data="district_Южный Падун")]
        ])
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Вихоревка", callback_data="district_Вихоревка")],
            [InlineKeyboardButton(text="Озёрный", callback_data="district_Озёрный")]
        ])
    await callback.message.edit_text("Выбери точное место:", reply_markup=kb)
    await callback.answer()

# Выбор района (2 уровень - сам район)
@dp.callback_query(Registration.district, F.data.startswith("district_"))
async def reg_district_final(callback: CallbackQuery, state: FSMContext):
    district = callback.data.replace("district_", "")
    await state.update_data(district=district)
    await callback.message.edit_text("Выбери до 3-х субкультур:", reply_markup=get_subcultures_kb([]))
    await state.update_data(subcultures=[])
    await state.set_state(Registration.subcultures)
    await callback.answer()

# Выбор субкультур
@dp.callback_query(Registration.subcultures, F.data.startswith("sub_"))
async def reg_subcultures(callback: CallbackQuery, state: FSMContext):
    if callback.data == "sub_done":
        data = await state.get_data()
        if not data.get("subcultures"):
            await callback.answer("Выбери хотя бы одну!", show_alert=True)
            return
        await callback.message.edit_text("Отправь свои фото (до 3-х). Сначала отправь главное фото.\nКогда закончишь — напиши /done")
        await state.set_state(Registration.photo)
        await callback.answer()
        return

    sub = callback.data.replace("sub_", "")
    data = await state.get_data()
    selected = data.get("subcultures", [])

    if sub in selected:
        selected.remove(sub)
    else:
        if len(selected) >= 3:
            await callback.answer("Максимум 3 субкультуры!", show_alert=True)
            return
        selected.append(sub)

    await state.update_data(subcultures=selected)
    await callback.message.edit_reply_markup(reply_markup=get_subcultures_kb(selected))
    await callback.answer()

# Фото
@dp.message(Registration.photo, F.photo)
async def reg_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])
    if len(photos) >= 3:
        await message.answer("Ты уже отправил 3 фото. Напиши /done, чтобы продолжить.")
        return
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    await message.answer(f"Фото добавлено ({len(photos)}/3). Отправь еще или напиши /done.")

@dp.message(Registration.photo, F.text == "/done")
async def reg_photo_done(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("photos"):
        await message.answer("Нужно хотя бы одно фото!")
        return
    await message.answer("Напиши пару слов о себе (или напиши /skip, чтобы пропустить).")
    await state.set_state(Registration.description)

@dp.message(Registration.description)
async def reg_desc(message: Message, state: FSMContext):
    desc = "" if message.text == "/skip" else message.text
    await state.update_data(description=desc)
    await message.answer("Укажи свой пол:", reply_markup=get_gender_kb())
    await state.set_state(Registration.gender)

# Пол
@dp.callback_query(Registration.gender, F.data.startswith("gender_"))
async def reg_gender(callback: CallbackQuery, state: FSMContext):
    gender = callback.data.replace("gender_", "")
    await state.update_data(gender=gender)
    await callback.message.edit_text("Кого ты хочешь найти?", reply_markup=get_looking_for_kb(gender))
    await callback.answer()

# Кого ищет + Подтверждение
@dp.callback_query(Registration.looking_for, F.data.startswith("look_"))
async def reg_looking(callback: CallbackQuery, state: FSMContext):
    look = callback.data.replace("look_", "")
    await state.update_data(looking_for=look)
    
    data = await state.get_data()
    text = (f"Проверь свою анкету:\n\n"
            f"<b>{data['name']}, {data['age']}, {data['district']}</b>\n"
            f"Субкультуры: {', '.join(data['subcultures'])}\n"
            f"О себе: {data['description'] or '—'}\n\n"
            f"Всё верно?")
    
    await callback.message.answer_photo(photo=data['photos'][0], caption=text, parse_mode="HTML", reply_markup=get_confirm_kb())
    await callback.message.delete()
    await state.set_state(Registration.confirm)
    await callback.answer()

# Сохранение анкеты
@dp.callback_query(Registration.confirm, F.data == "confirm_yes")
async def reg_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photos_str = ",".join(data['photos'])
    subs_str = ",".join(data['subcultures'])
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (user_id, username, name, age, district, subcultures, photos, description, gender, looking_for, is_approved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (callback.from_user.id, callback.from_user.username, data['name'], data['age'], data['district'], subs_str, photos_str, data['description'], data['gender'], data['looking_for']))
        await db.commit()

    await callback.message.answer("✅ Анкета отправлена на проверку! Ожидай одобрения.")
    await state.clear()
    await callback.answer()

@dp.callback_query(Registration.confirm, F.data == "confirm_no")
async def reg_restart(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await start_registration(callback.message, state)
    await callback.answer()

# --- Заглушки для остальных кнопок ---
@dp.message(F.text.in_({"1 🔍 Смотреть анкеты", "4 🚀 Поднять в топ", "5 ⭐ Поднять в топ", "2 📝 Заполнить заново", "3 🖼 Изменить фото", "4 ✏️ Изменить текст", "3 🚪 Я больше не хочу никого искать"}))
async def stub_actions(message: Message):
    await message.answer("⏳ Эта функция появится в следующем шаге.")

async def main():
    await init_db()
    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
