import asyncio
import logging
import sys

from aiogram import Dispatcher

from handlers.knowncommands import commands
from handlers.help import help_router
from handlers.othermessages import other

from bot import bot


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp = Dispatcher()

    dp.include_routers(
        commands,
        help_router,
        other
    )

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())