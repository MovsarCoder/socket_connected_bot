import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats

from bot.keyboards.commands import commands
from bot.routers import router
from bot.services.database import createTable

from core.config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        createTable()
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit()')
