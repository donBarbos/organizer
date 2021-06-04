import sqlite3
from datetime import datetime

from loguru import logger

conn = sqlite3.connect('../multitask.db')
cursor = conn.cursor()


def init_database():
    """создание базы данных."""
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    logger.info('init database multitask.db')
    conn.commit()


async def join(user_id: int, name: str):
    """заносим нового пользователя в БД."""
    cursor.execute(f'INSERT OR IGNORE INTO Users VALUES({user_id}, "{name}")')
    logger.info(f'new user added | user_id: {user_id}; name: {name}')
    conn.commit()


async def verification(user_id: int) -> bool:
    """проверяем есть ли пользователь в БД."""
    cursor.execute(f'SELECT user_id FROM Users WHERE user_id={user_id}')
    response = cursor.fetchall()
    conn.commit()
    if response:
        return True
    else:
        return False


async def get_weekly_affairs(user_id: int, weekday: int, time: str, text: str):
    """создаем еженедельное напоминание."""
    cursor.execute(f'SELECT * FROM WeeklyAffairs WHERE user_id={user_id}')
    response = cursor.fetchall()
    num = len(list(response)) + 1
    note_id = user_id + num
    cursor.execute(f'INSERT INTO WeeklyAffairs VALUES({user_id}, {note_id}, {weekday}, {time}, "{text}")')
    logger.info(f'create weekly affairs | user_id: {user_id}; note_id: {note_id}')
    conn.commit()


async def get_affair(user_id: int, date: str, time: str, text: str):
    """создаем заметку."""
    cursor.execute(f'SELECT * FROM Affairs WHERE user_id={user_id}')
    response = cursor.fetchall()
    num = len(list(response)) + 1
    note_id = user_id + num
    cursor.execute(f'INSERT INTO Affairs VALUES({user_id}, {note_id}, {date}, {time}, "{text}")')
    logger.info(f'create affairs | user_id: {user_id}; note_id: {note_id}')
    conn.commit()


async def get_quick_affair(user_id: int, timer: int, text: str):
    """создаем заметку, которая посылается через таймер."""
    cursor.execute(f'INSERT INTO Affairs VALUES({user_id}, {timer}, "{text}")')
    logger.info(f'create quick affairs | user_id: {user_id}; timer: {timer}')
    conn.commit()


async def get_list_today(user_id: int):
    """возвращает список заметок на сегодня."""
    index = 1
    list_today = []
    weekday = datetime.now().weekday()
    cursor.execute(f'SELECT text, time FROM WeeklyAffairs WHERE user_id={user_id} AND weekday={weekday}')
    records = cursor.fetchall()
    if records:
        for row in records:
            for elem in row[::2]:
                elem_list_today = str(index) + '. ' + elem + '. Время: ' + row[1]
                list_today.append(elem_list_today)
                index += 1
        response = True
    else:
        response = False

    today = datetime.now().date()
    cursor.execute(f'SELECT text, time FROM Affairs WHERE user_id={user_id} AND date="{today}"')
    records = cursor.fetchall()
    if records:
        for row in records:
            for elem in row[::2]:
                elem_list_today = str(index) + '. ' + elem + '. Время: ' + str(row[1])
                list_today.append(elem_list_today)
                index += 1
        return list_today
    else:
        if response:
            return list_today
        else:
            return False

    conn.commit()
