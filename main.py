import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, ADMIN_ID
from database import init_db, DB_PATH
from keyboards import get_main_menu_kb, get_my_profile_kb, get_new_user_kb

bot = Bot(token=9168726092:AAFiZen2ib0q7aWldD_MVJT8cX2f1H7ISoc)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET username = ?, last_seen = CURRENT_TIMESTAMP WHERE user_id = ?",
            (message.from_user.username, message.from_user.id)
        )
        await db.commit()

        async with db.execute(
            "SELECT is_approved, is_banned FROM users WHERE user_id = ?",
            (message.from_user.id,)
        ) as cursor:
            row = await cursor.fetchone()

    if row is None:
        await message.answer(
            f"Привет, {message.from_user.first_name}!\n\n"
            "Это <b>Свои Люди Братск | Знакомства 🖤</b>\n\n"
            "Здесь ты можешь найти своих людей из Братска и Братского района.\n"
            "Нажми кнопку ниже, чтобы создать анкету.",
            parse_mode="HTML",
            reply_markup=get_new_user_kb()
        )
        return

    is_approved, is_banned = row

    if is_banned:
        await message.answer("🚫 <b>Ты забанен</b>", parse_mode="HTML")
        return

    if not is_approved:
        await message.answer("⏳ <b>Твоя анкета на проверке</b>", parse_mode="HTML")
        return

    await show_main_menu(message)

async def show_main_menu(message: Message):
    await message.answer(
        "Подождем пока кто-то увидит твою анкету...\n\n"
        "1. Смотреть анкеты.\n"
        "2. Моя анкета.\n"
        "3. Я больше не хочу никого искать.\n"
        "***\n"
        "4. Поднять в топ 🚀",
        reply_markup=get_main_menu_kb()
    )

# --- Обработка кнопки "Моя анкета" ---
@dp.message(F.text == "2 👤 Моя анкета")
async def show_my_profile(message: Message):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT name, age, district, photos, description FROM users WHERE user_id = ?",
            (message.from_user.id,)
        ) as cursor:
            user = await cursor.fetchone()

    if not user:
        await message.answer("Анкета не найдена.")
        return

    name, age, district, photos, description = user
    photo_id = photos.split(',')[0] if photos else None
    
    text = f"Так выглядит твоя анкета:\n\n<b>{name}, {age}, {district}</b>\n{description or ''} ❤️"

    if photo_id:
        await message.answer_photo(
            photo=photo_id,
            caption=text,
            parse_mode="HTML",
            reply_markup=get_my_profile_kb()
        )
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=get_my_profile_kb())

# --- Заглушки для остальных кнопок (чтобы бот не молчал) ---
@dp.message(F.text.in_({
    "1 🔍 Смотреть анкеты", "4 🚀 Поднять в топ", "5 ⭐ Поднять в топ",
    "2 📝 Заполнить заново", "3 🖼 Изменить фото", "4 ✏️ Изменить текст",
    "📝 Создать анкету", "3 🚪 Я больше не хочу никого искать"
}))
async def stub_actions(message: Message):
    await message.answer("⏳ Эта функция появится в следующем шаге (код ещё пишется).")

async def main():
    await init_db()
    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())