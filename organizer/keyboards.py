from aiogram import types
from aiogram.types import InlineKeyboardButton


# клавиатура для ознакомления с кодом
btn_link = types.InlineKeyboardButton(text="Перейти на GitHub", url="https://github.com/DONSIMON92/organizer")
keyboard_link = types.InlineKeyboardMarkup().add(btn_link)

# клавиатура с настройками
# btn_name = types.InlineKeyboardButton(text=f'имя: {name}')
# btn_lang = types.InlineKeyboardButton(text='язык: {lang}')
# keyboard_settings = types.InlineKeyboardMarkup().add(btn_link)

# клавиатура для выбора типа заметки
btn_clock = InlineKeyboardButton("⏰ да", callback_data="note")
btn_timer = InlineKeyboardButton("⌛ нет", callback_data="weekly_note")
