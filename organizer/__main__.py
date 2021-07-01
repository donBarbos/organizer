import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import executor
from loguru import logger
import uvloop  # running only linux

from .commands import set_default_commands
from .db import Database
from .handlers import setup

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logger.add('logs/debug.log', format='{time} {level} {message}', level='DEBUG', rotation='10 KB', compression='zip')


async def startup(dispatcher: Dispatcher):
    """ initialization """
    await set_default_commands(dispatcher)
    await db.init_database()
    await setup(dispatcher, bot, db)


async def shutdown(dispatcher: Dispatcher):
    """ and need to close Redis and PostgreSQL connection when shutdown """
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await db.close_database()


if __name__ == '__main__':
    token = os.environ.get('BOT_TOKEN')
    bot = Bot(token=token, parse_mode='html')
    loop = asyncio.get_event_loop()
    storage = RedisStorage2(os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'), db=None)
    dp = Dispatcher(bot, loop=loop, storage=storage)
    db = Database(name=os.environ.get('PG_NAME'),
                  user=os.environ.get('PG_USER'),
                  password=os.environ.get('PG_PASSWORD'),
                  host=os.environ.get('PG_HOST'),
                  port=os.environ.get('PG_PORT'),
                  loop=loop,
                  pool=None)

    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
