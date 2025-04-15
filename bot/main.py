import asyncio
import logging

from loader import bot, main_router, dp


async def main():
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    asyncio.run(main())
