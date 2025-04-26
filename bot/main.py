import asyncio
import logging

from loader import loader, bot, clear_webhook


async def main():
    # await dp.start_polling(bot)
    runner = await loader()
    # print(await bot.get_webhook_info())

    try:
        await asyncio.Future()
    finally:
        await runner.cleanup()
        # Очищаем вебхук, на всякий случай
        await clear_webhook(bot_instance=bot)
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    asyncio.run(main())
