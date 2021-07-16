import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import uvloop  # running only linux

from organizer.database import Database


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
token = os.getenv("BOT_TOKEN")
bot = Bot(token=token, parse_mode="html")
loop = asyncio.get_event_loop()
storage = RedisStorage2(os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT"), db=5)
dp = Dispatcher(bot, loop=loop, storage=storage)
db = Database(
    name=os.getenv("PG_NAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    loop=loop,
    pool=None,
)
