import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton

from organizer.__main__ import bot, db, dp
from organizer.scan import search_time


# async def setup(dispatcher: Dispatcher, bot, db):
#     dispatcher.register_message_handler(start_message, commands=['start'], bot=bot, db=db)
#     dispatcher.register_message_handler(give_info, commands=['help', 'info'], bot=bot)
#     dispatcher.register_message_handler(give_list_today, commands=['today'], bot=bot, db=db)


@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    """приветственное сообщение."""
    if await db.verification(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            "Привет, мы уже работали раньше.\n" "Ваши записи сохранены.\n",
        )
    else:  # проверка наличия имени, фамилии или никнейма
        if message.from_user.first_name != "None":
            name = message.from_user.first_name
        elif message.from_user.username != "None":
            name = message.from_user.username
        elif message.from_user.last_name != "None":
            name = message.from_user.last_name
        else:
            name = ""
        await db.add_users(message.from_user.id, name)
        await bot.send_sticker(
            message.chat.id,
            "CAACAgIAAxkBAAIEqF5VL5ozeLnmwSaOJAbKQ" "DQAAfidjQACYwkAAgk7OxMAAVFVxKRh8u0YBA",
        )
        await bot.send_message(
            message.chat.id,
            "[О боте]\n"
            "Это приложение создано для планирования дел. "
            "С помощью данного бота вы можете создавать заметки. "
            "А в установленное время вам будут приходить уведомления.\n"
            "Чтобы ознакомиться с командами нажмите /commands.",
        )

    await bot.send_message(message.chat.id, "🕐 В ожидании вашего сообщения")


@dp.message_handler(commands=("help", "info"))
async def give_info(message: types.Message):
    """цель данного бота."""
    await bot.send_message(
        message.chat.id,
        "[О боте]\n Это приложение создано для планирования дел."
        "С помощью данного бота вы можете создавать заметки"
        "А в установленное время вам будут приходить уведомления.\n"
        "Чтобы ознакомиться с командами нажмите /commands.\n\n"
        "----------------------------------------------------"
        "Полный список команд, на которые отвечает бот:\n\n"
        "/help или /info - информация о боте и справка\n"
        "/today - вывести список дел на сегодня\n"
        "/settings - ваши настройки"
        "/contacts - получить ссылку на код проекта",
    )


# @dp.message_handler(commands='today')
async def give_list_today(message: types.Message, bot, db):
    """вывод списка дел, запланированных на сегодня."""
    list_today = await db.get_list_today(message.from_user.id)
    if list_today:
        list_today = "\n".join(list_today)
        await bot.send_message(message.chat.id, "Список дел на сегодня:\n" f"{list_today}")
    else:
        await bot.send_message(message.chat.id, "на сегодня записей не найдено")


# @dp.message_handler(commands='contacts')
async def give_contacts(message: types.Message, bot):
    """ссылка на код проекта."""
    btn_link = types.InlineKeyboardButton(text="Перейти на GitHub", url="https://github.com/DONSIMON92/organizer-bot")
    keyboard_link = types.InlineKeyboardMarkup().add(btn_link)
    await bot.send_message(message.chat.id, "Код проекта доступен на GitHub", reply_markup=keyboard_link)


# @dp.message_handler(commands='settings')
async def give_settings(message: types.Message, bot, db):
    """справка по настройкам."""
    name = await db.get_name(message.from_user.id)
    lang = await db.get_lang(message.from_user.id)
    btn_name = types.InlineKeyboardButton(text=f"имя: {name}")
    btn_lang = types.InlineKeyboardButton(text=f"язык: {lang}")
    keyboard_settings = types.InlineKeyboardMarkup().add(btn_name, btn_lang)
    await bot.send_message(message.chat.id, "Настройки ⚙️", reply_markup=keyboard_settings)


class Form(StatesGroup):
    wait_text = State()
    wait_type = State()
    wait_time_txt = State()


# @dp.message_handler(commands='new')     # дописать фильтр отправляемых заметок
async def get_task(message: types.Message):
    await Form.wait_text.set()
    await message.answer("Отправьте текст")


# @dp.message_handler(state=Form.wait_text)
async def process_text(message: types.Message, state: FSMContext, bot):
    async with state.proxy() as data:
        data["wait_text"] = message.text

    await Form.next()
    keyboard_time = types.InlineKeyboardMarkup()
    btn_timer = InlineKeyboardButton("⌛ таймер", callback_data="timer")
    btn_clock = InlineKeyboardButton("⏰ часы", callback_data="clock")
    keyboard_time.add(btn_timer, btn_clock)
    await bot.send_message(
        message.chat.id,
        "🤔 Как вы желаете настроить время получения уведомления?\n"
        "(с помощью таймера или установки определенного времени)",
        reply_markup=keyboard_time,
    )


# @dp.callback_query_handler(state=Form.wait_type)
async def process_type(callback_query: types.CallbackQuery, state: FSMContext, bot):
    current_state = await state.get_state()
    if current_state == "timer":
        async with state.proxy() as data:
            data["wait_type"] = "timer"
    else:
        await bot.send_message(callback_query.from_user.id, current_state)

    print(current_state)
    await bot.send_message(
        callback_query.from_user.id,
        "🕛 Напишите время, через которое вы получите напоминание.",
    )


# @dp.message_handler(state=Form.wait_time_txt)
async def process_timer(message: types.Message, state: FSMContext, bot):
    time_txt = message.text
    time_wait = await search_time(time_txt)  # поиск времени в тексте
    async with state.proxy() as data:
        data["wait_time_txt"] = time_wait
    await state.finish()
    await bot.send_message(f"✅ Новая задача успешно создана. Напоминание придет через {time_wait} сек.")
    await asyncio.sleep(time_wait)


# @dp.callback_query_handler(lambda c: c.data == 'clock')
async def get_btn_clock(callback_query: types.CallbackQuery, bot):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "🕛 Выберите дату и время")


# @dp.message_handler()
async def unknown_message(message: types.Message, bot):
    if not message.is_command():
        await bot.send_message(message.chat.id, "❌ Я не умею работать с данным форматом.")
    else:
        await message.answer("❌ Некорректная команда.\n" "Чтобы ознакомиться с командами нажмите на /commands")
