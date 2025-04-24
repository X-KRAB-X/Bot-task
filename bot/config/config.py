import dotenv
import os

from aiogram.types import BotCommand


if dotenv.find_dotenv():
    dotenv.load_dotenv()
else:
    exit('Не найдет файл .env')

BOT_TOKEN = os.getenv('BOT_TOKEN')

# -- Webhooks --
WEB_SERVER_HOST = '127.0.0.1'
WEB_SERVER_PORT = 8000

WEBHOOK_PATH = '/webhook'
# WEBHOOK_SECRET
WEBHOOK_URL = 'https://andrey-bokarev.ru'


# -- API --
API_URL = 'https://jsonplaceholder.typicode.com/'


# -- DATABASE --
DATABASE_URL = 'postgresql+asyncpg://andrey:joker2500@localhost/test_base'


# -- Bot commands --
BOT_COMMANDS = [
    BotCommand(command='/start', description='Приветствие'),
    BotCommand(command='/help', description='Помощь по командам'),
    BotCommand(command='/get', description='Сделать запрос к API')
]
