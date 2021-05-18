import time
import re

from aiogram import Bot, types  # подключение библиотеки для работы с telegram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes, callback_query
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from db import Create_database, Verification, Join, Get_Affair, Get_QuickAffair # подключение модулей для работы с БД
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

Create_database()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user_id = message.from_user.id  # считывание id
    if Verification(user_id):
        await bot.send_message(message.chat.id, 'Привет, мы с тобой уже работали раньше.\nВаши записи сохранены.')
    else:
        if message.from_user.first_name != 'None':  # проверка наличия имени, фамилии или юзернейма
            name = message.from_user.first_name
        elif message.from_user.username != 'None':
            name = message.from_user.username
        elif message.from_user.last_name != 'None':
            name = message.from_user.last_name
        else:
            name = ''
        Join(message.from_user.id, name)
        await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIEqF5VL5ozeLnmwSaOJAbKQDQAAfidjQACYwkAAgk7OxMAAVFVxKRh8u0YBA')
        await bot.send_message(message.chat.id, 'Этот бот нужен для создания заметок.\n'
                                                'Он может хранить ваши заметки и отправлять вам напоминания.\n'
                                                'Для работы с ним не нужна дополнительная авторизация,\n'
                                                'Вы можете проверять записи и получать уведомления.\n'
                                                'Чтобы глубже ознакомиться с функционалом нажмите на /commands')

    await bot.send_message(message.chat.id, '🕐 В ожидании вашего сообщения')
        

@dp.message_handler(commands=['commands'])
async def list_commands(message: types.Message):
    await bot.send_message(message.chat.id,
                           'полный список команд, на которые отвечает бот:\n\n'
                           '/info - информация о боте\n'
                           '/contacts - информация о создателе и код программы\n'
                           '/today - список заметок на день\n'
                           'чтобы создать заметку, просто напишите мне сообщение.')


@dp.message_handler(commands=['today'])
async def today(message: types.Message):
    await bot.send_message(message.chat.id, 'список дел на сегодня\n\n')


@dp.message_handler(commands=['info'])
async def give_info(message: types.Message):
    await bot.send_message(message.chat.id, '[О боте]\nЭто приложение создано для планирования дел.'
                                            'Здесь вы можете создать своё расписание и добавлять новые заметки.'
                                            'В установленное время вам будет приходить уведомление.\n'
                                            'Также код проекта доступен на Github')


@dp.message_handler(commands=['contacts'])
async def contacts(message: types.Message):
    btn_link = types.InlineKeyboardButton(text='Перейти на GitHub', url='https://github.com/DONSIMON92/bot-organizer')
    keyboard_link = types.InlineKeyboardMarkup().add(btn_link)
    await bot.send_message(message.chat.id, 'Код проекта доступен на GitHub', reply_markup=keyboard_link)


@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    await bot.send_message(message.chat.id, '❌ Я не умею работать с фото')


@dp.message_handler(content_types=['text'])  # дописать фильтр отправляемых заметок
async def get_task(message: types.Message):
    if not message.is_command():
        text = message.text
        keyboard_time = types.InlineKeyboardMarkup()
        btn_timer = InlineKeyboardButton('⌛ таймер', callback_data='timer')
        btn_clock = InlineKeyboardButton('⏰ часы', callback_data='clock')
        keyboard_time.add(btn_timer, btn_clock)
        await bot.send_message(message.chat.id, '🤔 Как вы желаете настроить время получения уведомления?\n'
                                                '(с помощью таймера или установки определенного времени)', reply_markup=keyboard_time)
    else:
        await message.answer('❌ Я не знаю такой команды.\n'
                             'Чтобы ознакомиться с командами нажмите на /commands')


@dp.callback_query_handler(lambda c: c.data == 'timer')
async def get_btn_timer(callback_query: types.CallbackQuery):
    #await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🕛 Напишите время, через которое вы получите напоминание.')
   

@dp.message_handler(content_types=['text'])
async def get_timer(message: types.Message):
    time_txt = message.text

    time_txt = re.sub(r'и ', '', time_txt)
    time_txt = re.sub(r'через ', '', time_txt)

    patterns_hour = ['часов', 'часа', 'час', 'ч']
    patterns_minute = ['минута', 'минуты', 'минуту', 'минут', 'мин', 'м']
    patterns_second = ['секунда', 'секунды', 'секунду', 'секунд', 'сек', 'с']

    try:
        for pattern in patterns_hour:
            if re.search(pattern, time_txt, flags=re.IGNORECASE):
                result = re.split(pattern, time_txt, flags=re.IGNORECASE)
                time_from_hour = 3600 * int(re.search(r'\d{1,3}', result[0]).group(0))  # в первом элементе время в часах
                time_txt = str(result[1])  # второй элемент будет обрабатываться дальше
                break
    except AttributeError:
        time_from_hour = 0
        print('Error - no pattern(hour) found')

    try:
        for pattern in patterns_minute:
            if re.search(pattern, time_txt, flags=re.IGNORECASE):
                result = re.split(pattern, time_txt, flags=re.IGNORECASE)
                time_from_min = 60 * int(re.search(r'\d{1,3}', result[0]).group(0))
                time_txt = str(result[1])
                break
    except AttributeError:
        time_from_min = 0
        print('Error - no pattern(minute) found')

    try:
        for pattern in patterns_second:
            if re.search(pattern, time_txt, flags=re.IGNORECASE):
                result = re.split(pattern, time_txt, flags=re.IGNORECASE)
                time_from_sec = int(re.search(r'\d{1,6}', result[0]).group(0))
                break
    except AttributeError:
        time_from_sec = 0
        print('Error - no pattern(second) found')

    time_wait = time_from_hour + time_from_min + time_from_sec
    await message_handler.answer("✅ Новая задача успешно создана."
                                f"Напоминание придет через {time_wait/3600} ч.")
    Get_QuickAffair(user_id, time_wait, data)


@dp.callback_query_handler(lambda c: c.data == 'clock')
async def get_btn_clock(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🕛 Выберите дату и время')


if __name__ == '__main__':  # зацикливание бота
    executor.start_polling(dp)
