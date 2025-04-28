import os

from aiogram.types import BotCommand


BOT_TOKEN = os.getenv('BOT_TOKEN')
print(os.getenv('GOOGLE_KEY_PATH')) # Проверка
print(os.getenv('DOMAIN_NAME')) # Проверка

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
    DATABASE_URL = 'postgresql://bot_user@db/bot_db'


# -- GOOGLE SHEETS API --
CREDENTIALS_FILE = os.getenv('GOOGLE_KEY_PATH')
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
