"""
Модуль для обращения по http к API.
Работает асинхронно.
"""


from aiohttp import ClientSession


async def get_json_response(url: str, query: str):
    """
    Получает url и query, после чего делает запрос и возвращает JSON-ответ.
    """
    async with ClientSession() as session:
        async with session.get(url + query) as response:
            return await response.json()
