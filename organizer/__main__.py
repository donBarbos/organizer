from aiogram import Dispatcher
from aiogram.utils import executor
from loguru import logger
from organizer.commands import set_default_commands
from organizer.loader import db
from organizer.loader import dp


async def startup(dispatcher: Dispatcher):
    """initialization"""
    await db.init_database()
    await set_default_commands(dispatcher)
    logger.info("bot started")


async def shutdown(dispatcher: Dispatcher):
    """and need to close Redis and PostgreSQL connection when shutdown"""
    await db.close_database()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info("bot finished")


if __name__ == "__main__":
    logger.add(
        "logs/debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="30 KB",
        compression="zip",
    )
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
