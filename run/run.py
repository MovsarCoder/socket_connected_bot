import asyncio
import logging
from aiogram.types import BotCommandScopeAllPrivateChats
from database.db import createTable
from aiogram import Bot, Dispatcher
from allFunctions import router
from bot_started_commands.bot_commands import commands
from config.get_token import TOKEN

async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()

    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())


if __name__ == "__main__":

    try:

        createTable()

        asyncio.run(main())

    except KeyboardInterrupt:

        print('exit()')
