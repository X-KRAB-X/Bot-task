import re


async def _from_camel_to_snake(string: str) -> str:
    """
    Функция-исполнитель преобразования из CamelCase в snake_case.
    """

    return re.sub(pattern=r'(.)(?=[A-Z])', repl=r'\1_', string=string).lower()


async def from_camel_to_snake_json_keys(json_dict: dict) -> dict:
    """
    Преобразовывает все ключи в словаре(JSON) из CamelCase в snake_case.
    """

    new_json_dict = {}
    for key, value in json_dict.items():
        new_json_dict[await _from_camel_to_snake(key)] = value

    return new_json_dict
