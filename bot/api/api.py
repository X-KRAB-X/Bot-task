from aiohttp import ClientSession


async def get_json_response(url: str, query: str):
    """
    Получает url и query, после чего делает запрос и валидирует(?) ответ.
    """
    async with ClientSession() as session:
        async with session.get(url + query) as response:
            return await response.json()
