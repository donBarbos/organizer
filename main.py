import re
import os
import asyncio

from loguru import logger
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from db import init_database, verification, join, get_affair, get_quick_affair, get_weekly_affairs, get_list_today

logger.add('logs/debug.log', format='{time} {level} {message}', level='DEBUG', rotation='10 KB', compression='zip')


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

init_database()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if await verification(message.from_user.id):
        await bot.send_message(message.chat.id, 'Привет, мы уже работали раньше.\n'
                                                'Ваши записи сохранены.\n')
    else:   # проверка наличия имени, фамилии или юзернейма
        if message.from_user.first_name != 'None':
            name = message.from_user.first_name
        elif message.from_user.username != 'None':
            name = message.from_user.username
        elif message.from_user.last_name != 'None':
            name = message.from_user.last_name
        else:
            name = ''
        await join(message.from_user.id, name)
        await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIEqF5VL5ozeLnmwSaOJAbKQ'
                                                'DQAAfidjQACYwkAAgk7OxMAAVFVxKRh8u0YBA')
        await bot.send_message(message.chat.id, '[О боте]\n'
                                                'Это приложение создано для планирования дел.'
                                                'С помощью данного бота вы можете создавать заметки'
                                                'А в установленное время вам будут приходить уведомления.\n'
                                                'Чтобы ознакомиться с командами нажмите /commands.')

    await bot.send_message(message.chat.id, '🕐 В ожидании вашего сообщения')


@dp.message_handler(commands=['commands'])
async def list_commands(message: types.Message):
    await bot.send_message(message.chat.id, 'Полный список команд, на которые отвечает бот:\n\n'
                                            '/new - сделать новую заметку\n'
                                            '/info - информация о боте\n'
                                            '/today - список заметок на день\n'
                                            '/contacts - информация о создателе и код программы\n')


@dp.message_handler(commands=['today'])
async def give_list_today(message: types.Message):
    list_today = await get_list_today(message.from_user.id)
    if list_today is False:
        await bot.send_message(message.chat.id, 'на сегодня записей не найдено')
    else:
        await bot.send_message(message.chat.id, 'Список дел на сегодня:\n'
                                                f'{list_today}')


@dp.message_handler(commands=['info', 'help'])
async def give_info(message: types.Message):
    await bot.send_message(message.chat.id, '[О боте]\n'
                                            'Это приложение создано для планирования дел.'
                                            'С помощью данного бота вы можете создавать заметки'
                                            'А в установленное время вам будут приходить уведомления.\n'
                                            'Чтобы ознакомиться с командами нажмите /commands.')


@dp.message_handler(commands=['contacts'])
async def give_contacts(message: types.Message):
    btn_link = types.InlineKeyboardButton(text='Перейти на GitHub', url='https://github.com/DONSIMON92/organizer-bot')
    keyboard_link = types.InlineKeyboardMarkup().add(btn_link)
    await bot.send_message(message.chat.id, 'Код проекта доступен на GitHub', reply_markup=keyboard_link)


class Form(StatesGroup):
    wait_text = State()
    wait_type = State()
    wait_time_txt = State()


@dp.message_handler(commands='new')     # дописать фильтр отправляемых заметок
async def get_task(message: types.Message):
    await Form.wait_text.set()
    await message.answer('Отправьте текст')


@dp.message_handler(state=Form.wait_text)
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wait_text'] = message.text

    await Form.next()
    keyboard_time = types.InlineKeyboardMarkup()
    btn_timer = InlineKeyboardButton('⌛ таймер', callback_data='timer')
    btn_clock = InlineKeyboardButton('⏰ часы', callback_data='clock')
    keyboard_time.add(btn_timer, btn_clock)
    await bot.send_message(message.chat.id, '🤔 Как вы желаете настроить время получения уведомления?\n'
                                            '(с помощью таймера или установки определенного времени)',
                                            reply_markup=keyboard_time)


@dp.callback_query_handler(state=Form.wait_type)
async def process_type(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['wait_type'] = bot.callback_query.message.answer

    print(callback_query.message.answer)
    await bot.send_message(callback_query.from_user.id, '🕛 Напишите время, через которое вы получите напоминание.')


@dp.message_handler(state=Form.wait_time_txt)
async def process_timer(message: types.Message, state: FSMContext):
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
                time_from_hour = 3600 * int(re.search(r'\d{1,3}',   # в первом элементе время в часах
                                            result[0]).group(0))
                time_txt = str(result[1])  # второй элемент передаётся дальше
                break
    except AttributeError:
        time_from_hour = 0
        logger.debug('Error - no pattern(hour) found')

    try:
        for pattern in patterns_minute:
            if re.search(pattern, time_txt, flags=re.IGNORECASE):
                result = re.split(pattern, time_txt, flags=re.IGNORECASE)
                time_from_min = 60 * int(re.search(r'\d{1,3}',
                                         result[0]).group(0))
                time_txt = str(result[1])
                break
    except AttributeError:
        time_from_min = 0
        logger.debug('Error - no pattern(minute) found')

    try:
        for pattern in patterns_second:
            if re.search(pattern, time_txt, flags=re.IGNORECASE):
                result = re.split(pattern, time_txt, flags=re.IGNORECASE)
                time_from_sec = int(re.search(r'\d{1,6}',
                                    result[0]).group(0))
                break
    except AttributeError:
        time_from_sec = 0
        logger.debug('Error - no pattern(second) found')

    time_wait = time_from_hour + time_from_min + time_from_sec
    async with state.proxy() as data:
        data['wait_time_txt'] = time_wait
    await state.finish()
    await bot.send_message(f'✅ Новая задача успешно создана. Напоминание придет через {time_wait} сек.')
    await asyncio.sleep(time_wait)


@dp.callback_query_handler(lambda c: c.data == 'clock')
async def get_btn_clock(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           '🕛 Выберите дату и время')


@dp.message_handler()
async def unknown_message(message: types.Message):
    if not message.is_command():
        await bot.send_message(message.chat.id, '❌ Я не умею работать с данным форматом. '
                                                'Пришлите мне текстовое сообщение.')
    else:
        await message.answer('❌ Некорректная команда.\nЧтобы ознакомиться с командами нажмите на /commands')


# Альтернативный вариант
# @dp.message_handler()
# async def unknown_message(message: types.Message):
#     await bot.send_message(message.chat.id,
#                            '🤷 Не понимаю вас.' )


if __name__ == '__main__':
    executor.start_polling(dp)
