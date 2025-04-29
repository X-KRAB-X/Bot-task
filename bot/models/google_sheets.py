"""
Данный модуль предоставляет методы по созданию листов в Google Sheets.
Сами листы оформлены в виде "Название: Список полей"
"""


import logging
import asyncio

import gspread

from config.config import CREDENTIALS_FILE, SPREADSHEET_ID, SCOPES


# Данный словарь содержит в себе данные вида: "Лист": "Поля"
# Значения в списках взяты из Pydantic-моделей.
# Вложенные данные преобразованы в "плоский" формат.
sheets = {
    'users': [
        'telegram_user_id',
        'created_at',

        # user
        'user_id',
        'name',
        'username',
        'email',
        'phone',
        'website',
        
        # address
        'address_street',
        'address_suite',
        'address_city',
        'address_zipcode',

        # geo
        'address_geo_lat',
        'address_geo_lng',

        # company
        'company_name',
        'company_catchPhrase',
        'company_bs',
        ],

    'posts': ['telegram_user_id', 'created_at', 'post_id', 'user_id', 'title', 'body'],
    'comments': ['telegram_user_id', 'created_at', 'comment_id', 'post_id', 'name', 'email', 'body'],
    'albums': ['telegram_user_id', 'created_at', 'album_id', 'user_id', 'title'],
    'photos': ['telegram_user_id', 'created_at', 'photo_id', 'album_id', 'title', 'url', 'thumbnail_url'],
    'todos': ['telegram_user_id', 'created_at', 'todo_id', 'user_id', 'title', 'completed'],
}


async def _create_sheet_if_not_exists(spreadsheet, sheet_name: str, sheet_headers: list):
    """
    Функция-исполнитель.
    Проверяет, что лист существует. Если нет - создает его.

    :param spreadsheet: Объект электронной таблицы.
    :param sheet_name: Имя Листа.
    :param sheet_headers: Список с заголовками столбцов.
    :return:
    """

    # Если получится получить лист - ничего не делаем.
    # Иначе - создаем его.
    try:
        logging.info(f'Проверяю лист {sheet_name}')

        worksheet = await asyncio.to_thread(spreadsheet.worksheet, sheet_name)

        logging.info(f'Лист {sheet_name} существует.')
    except gspread.exceptions.WorksheetNotFound:
        logging.info(f'Не удалось получить лист {sheet_name}. Создаю..')

        worksheet = await asyncio.to_thread(spreadsheet.add_worksheet, title=sheet_name, rows=1000, cols=20)
        await asyncio.to_thread(worksheet.append_row, sheet_headers)


async def create_google_sheets():
    """
    Функция для создания листов в Google Sheets.
    Создает листы, если они не существуют.
    """

    try:
        # Создаем соединение.
        client = await asyncio.to_thread(gspread.service_account, filename=CREDENTIALS_FILE, scopes=SCOPES)

        # Получаем эл. таблицу
        spreadsheet = await asyncio.to_thread(client.open_by_key,SPREADSHEET_ID)
    except Exception as e:
        logging.error(f'Ошибка при попытке получения таблицы Google Sheets:\n{e}')
    else:
        for sheet_name, sheet_headers in sheets.items():
            await _create_sheet_if_not_exists(spreadsheet, sheet_name, sheet_headers)
