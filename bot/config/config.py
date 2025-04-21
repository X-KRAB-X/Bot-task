import dotenv
import os

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

# -- Webhooks --

# -- API --
API_URL = 'https://jsonplaceholder.typicode.com/'
