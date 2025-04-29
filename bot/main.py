"""
Главный исполняемый файл.
"""

import asyncio
import logging

from loader import loader, bot, clear_webhook


async def main():
    runner = await loader()

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
