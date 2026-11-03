from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_kb():
    """Клавиатура для главного меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1 🔍 Смотреть анкеты"),
                KeyboardButton(text="2 👤 Моя анкета")
            ],
            [
                KeyboardButton(text="3 🚪 Я больше не хочу никого искать"),
                KeyboardButton(text="4 🚀 Поднять в топ")
            ]
        ],
        resize_keyboard=True
    )

def get_my_profile_kb():
    """Клавиатура для экрана 'Моя анкета'"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1 🔍 Смотреть анкеты"),
                KeyboardButton(text="2 📝 Заполнить заново"),
                KeyboardButton(text="3 🖼 Изменить фото")
            ],
            [
                KeyboardButton(text="4 ✏️ Изменить текст"),
                KeyboardButton(text="5 ⭐ Поднять в топ")
            ]
        ],
        resize_keyboard=True
    )

def get_new_user_kb():
    """Клавиатура для нового пользователя (до создания анкеты)"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📝 Создать анкету")]],
        resize_keyboard=True
    )