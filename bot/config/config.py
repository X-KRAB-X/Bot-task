import dotenv
import os

if dotenv.find_dotenv():
    dotenv.load_dotenv()
else:
    exit('Не найдет файл .env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
