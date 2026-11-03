from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1 🔍 Смотреть анкеты"), KeyboardButton(text="2 👤 Моя анкета")],
            [KeyboardButton(text="3 🚪 Я больше не хочу никого искать"), KeyboardButton(text="4 🚀 Поднять в топ")]
        ],
        resize_keyboard=True
    )

def get_my_profile_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1 🔍 Смотреть анкеты"), KeyboardButton(text="2 📝 Заполнить заново"), KeyboardButton(text="3 🖼 Изменить фото")],
            [KeyboardButton(text="4 ✏️ Изменить текст"), KeyboardButton(text="5 ⭐ Поднять в топ")]
        ],
        resize_keyboard=True
    )

def get_new_user_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📝 Создать анкету")]],
        resize_keyboard=True
    )

def get_districts_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Центральный район", callback_data="dist_group_central")],
        [InlineKeyboardButton(text="Правобережный (Гидростроитель)", callback_data="dist_group_right")],
        [InlineKeyboardButton(text="Падунский район", callback_data="dist_group_padun")],
        [InlineKeyboardButton(text="Братский район", callback_data="dist_group_bratsk")]
    ])

def get_subcultures_kb(selected: list):
    options = [
        ("Гот", "🖤 Гот"), ("Альтушка / альт", "🎀 Альтушка"), ("Эмо", "💀 Эмо"),
        ("Металлист", "🤘 Металлист"), ("Панк", "🧷 Панк"), ("Рэйвер", "🎧 Рэйвер"),
        ("Анимешник / косплеер", "🌸 Аниме"), ("Обычный / без тега", "👤 Обычный")
    ]
    keyboard = []
    row = []
    for value, text in options:
        if value in selected:
            text = f"✅ {text}"
        row.append(InlineKeyboardButton(text=text, callback_data=f"sub_{value}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton(text="Готово ✅", callback_data="sub_done")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_gender_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Парень", callback_data="gender_male")],
        [InlineKeyboardButton(text="👩 Девушка", callback_data="gender_female")]
    ])

def get_looking_for_kb(gender: str):
    if gender == "male":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👫 Друга", callback_data="look_friend")],
            [InlineKeyboardButton(text="💑 Девушку", callback_data="look_partner")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👫 Друзей", callback_data="look_friend")],
            [InlineKeyboardButton(text="💑 Парня", callback_data="look_partner")]
        ])

def get_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Отправить на проверку", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="✏️ Заполнить заново", callback_data="confirm_no")]
    ])
