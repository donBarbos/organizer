from datetime import datetime

import asyncpg
from loguru import logger


class Database(object):
    def __init__(self, name, user, password, host, port, loop, pool: asyncpg.pool.Pool) -> None:
        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.loop = loop
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                database=name,
                user=user,
                password=password,
                host=host,
                port=port,
            )
        )

    async def init_database(self) -> None:
        """создание таблиц в БД."""
        with open('organizer/init.sql', 'r') as f:
            sql = f.read()
        await self.pool.execute(sql)
        logger.info('init database')

    async def close_database(self) -> None:
        await self.pool.close()
        logger.info('close database')

    async def add_user(self, user_id: int, name: str) -> None:
        """заносим нового пользователя в БД."""
        self.pool.execute(f"INSERT INTO Users VALUES({user_id}, '{name}')")
        logger.info(f'new user added | user_id: {user_id}; name: {name}')
        # self.pool.commit()

    async def verification(self, user_id: int) -> bool:
        """проверяем есть ли пользователь в БД."""
        # conn.execute(f'SELECT user_id FROM Users WHERE user_id={user_id}')
        response = self.pool.fetchrow(f'SELECT user_id FROM Users WHERE user_id={user_id}')
        if response:
            return True
        else:
            return False

    async def add_weekly_note(self, user_id: int, weekday: int, time: str, text: str) -> None:
        """создаем еженедельную заметку."""
        response = self.pool.fetch(f'SELECT * FROM WeeklyNotes WHERE user_id={user_id}')
        num = len(response) + 1
        note_id = user_id + num
        self.pool.execute(f"INSERT INTO WeeklyNotes VALUES({user_id}, {note_id}, {weekday}, '{time}', '{text}')")
        logger.info(f'create weekly notes | user_id: {user_id}; note_id: {note_id}')
        self.pool.commit()

    async def add_note(self, user_id: int, date: str, time: str, text: str) -> None:
        """создаем заметку."""
        response = self.pool.fetch(f'SELECT * FROM Notes WHERE user_id={user_id}')
        num = len(response) + 1
        note_id = user_id + num
        self.pool.execute(f"INSERT INTO Notes VALUES({user_id}, {note_id}, {date}, '{time}', '{text}')")
        logger.info(f'create notes | user_id: {user_id}; note_id: {note_id}')
        self.pool.commit()

    async def get_name(self, user_id: int) -> str:
        return self.pool.fetchval(f'SELECT name FROM Users WHERE user_id={user_id}')

    async def get_lang(self, user_id: int) -> str:
        return self.pool.fetchval(f'SELECT lang FROM Users WHERE user_id={user_id}')

    async def get_list_today(self, user_id: int) -> tuple:
        """узнаем список заметок на сегодня из 2х таблиц."""
        index = 1
        list_today = []  # сделать кортежем () и переделать логику
        weekday = datetime.now().weekday()
        records = self.pool.fetch(f'SELECT text, time FROM WeeklyNotes WHERE user_id={user_id} AND weekday={weekday}')
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
        records = self.pool.fetch(f"SELECT text, time FROM Notes WHERE user_id={user_id} AND date='{today}'")
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
                return False  # return list_today
