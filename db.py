import sqlite3
from datetime import datetime

from loguru import logger

conn = sqlite3.connect('multitask.db')
cursor = conn.cursor()


def init_database():
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    logger.info('init database multitask.db')
    conn.commit()


async def join(user_id, name):
    cursor.execute(f'INSERT OR IGNORE INTO Users VALUES({user_id}, "{name}")')
    logger.info(f'new user added | user_id: {user_id}; name: {name}')
    conn.commit()


async def verification(user_id):
    cursor.execute(f'SELECT user_id FROM Users WHERE user_id={user_id}')
    response = cursor.fetchall()
    conn.commit()
    if response:
        return True
    else:
        return False


async def get_weekly_affairs(user_id, weekday, time, text):
    cursor.execute(f'SELECT * FROM WeeklyAffairs WHERE user_id={user_id}')
    response = cursor.fetchall()
    num = len(list(response)) + 1
    note_id = user_id + num
    cursor.execute(f'INSERT INTO WeeklyAffairs VALUES({user_id}, {note_id}, {weekday}, {time}, "{text}")')
    logger.info(f'create weekly affairs | user_id: {user_id}; note_id: {note_id}')
    conn.commit()


async def get_affair(user_id, date, time, text):
    cursor.execute(f'SELECT * FROM Affairs WHERE user_id={user_id}')
    response = cursor.fetchall()
    num = len(list(response)) + 1
    note_id = user_id + num
    cursor.execute(f'INSERT INTO Affairs VALUES({user_id}, {note_id}, {date}, {time}, "{text}")')
    logger.info(f'create affairs | user_id: {user_id}; note_id: {note_id}')
    conn.commit()


async def get_quick_affair(user_id, timer, text):
    cursor.execute(f'INSERT INTO Affairs VALUES({user_id}, {timer}, "{text}")')
    logger.info(f'create quick affairs | user_id: {user_id}; timer: {timer}')
    conn.commit()


async def get_list_today(user_id):
    today = datetime.now().date()
    weekday = datetime.now().weekday()
    cursor.execute(f'SELECT * FROM WeeklyAffairs WHERE user_id={user_id} AND weekday={weekday}')
    cursor.execute(f'SELECT * FROM Affairs WHERE user_id={user_id} AND date={today}')
    records = cursor.fetchall()
    if records:
        for row in records:
            print('ID:', row[0])
            print('Имя:', row[1])
            print('Почта:', row[2])
            print('Добавлен:', row[3])
            print('Добавлен:', row[4])
            print('Зарплата:', row[5])
            print('Зарплата:', row[6], end='\n\n')
        # return something else...
    else:
        return False

    conn.commit()
