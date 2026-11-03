from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
