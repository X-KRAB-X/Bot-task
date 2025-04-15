import asyncio
import logging

from loader import loader, bot


async def main():
    # await dp.start_polling(bot)
    runner = await loader()
    print(bot.get_webhook_info())

    try:
        await asyncio.Future()
    finally:
        await runner.cleanup()
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    asyncio.run(main())
