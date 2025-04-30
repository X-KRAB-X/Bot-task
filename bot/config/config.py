"""
Внутренние настройки бота.
Данный модуль также служит сборником переменных окружения.
"""

import os

from aiogram.types import BotCommand


BOT_TOKEN = os.getenv('BOT_TOKEN')

# -- Webhooks --
WEB_SERVER_HOST = '127.0.0.1'
WEB_SERVER_PORT = 8000

WEBHOOK_PATH = '/webhook'
# WEBHOOK_SECRET
WEBHOOK_URL = os.getenv('DOMAIN_NAME')


# -- API --
API_URL = 'https://jsonplaceholder.typicode.com/'


# -- DATABASE --
if os.getenv('DATABASE_URL'):
    DATABASE_URL = os.getenv('DATABASE_URL')
else:
    DATABASE_URL = 'postgresql+asyncpg://bot_user:12345@db/bot_db'


# -- GOOGLE SHEETS API --
_CREDENTIALS_FILE_NAME = os.getenv('GOOGLE_KEY_NAME')
CREDENTIALS_FILE = os.path.join('/Bot-task', 'GH', _CREDENTIALS_FILE_NAME) # По умолчанию в контейнере /Bot-task находится в корне
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


# -- Bot commands --
BOT_COMMANDS = [
    BotCommand(command='/start', description='Приветствие'),
    BotCommand(command='/help', description='Помощь по командам'),
    BotCommand(command='/get', description='Сделать запрос к API'),
]
