from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("help", "Помощь"),
            types.BotCommand("today", "Список дел на сегодня"),
            types.BotCommand("settings", "Ваши настройки"),
            types.BotCommand("contacts", "Получить ссылку на код проекта"),
        ]
    )
