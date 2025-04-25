import logging
import json

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext

from sqlalchemy.exc import SQLAlchemyError

from api.api import get_json_response
from config.config import API_URL
from states.states import APIResponseStates
from keyboard.api_get_keyboard import api_get_keyboard, back_and_cancel_keyboard

# Pydantic
from models.pydantic_api import (
    UserModel,
    PostModel,
    CommentModel,
    AlbumModel,
    PhotoModel,
    TodoModel
)

from .utils import from_camel_to_snake_json_keys


custom_router = Router(name='custom_router')

# Для предоставления пользователю кол-ва доступных id. Также позволяет избежать HTTP 404
available_resources = {
    'users': 10,
    'posts': 100,
    'comments': 500,
    'albums': 100,
    'photos': 5000,
    'todos': 200
}


async def _get_api_data_and_save(db, pydantic_model, telegram_user_id, resource: str, resource_id: int) -> str:
    """
    Функция-исполнитель.
    Получает введенные данные и отправляет запрос с последующим сохранением в БД.

    :param db: Сервис БД для сохранения объекта.
    :param pydantic_model: Модель для валидации в зависимости от указанного URL.
    :param resource: Название URL, по которому был отправлен запрос.
    Таким образом указывается метод, который будет вызван для создания записи.
    :param resource_id: ID выбранного ресурса.

    :return: JSON-Pydantic модель с данными из БД
    """

    logging.info('Отправляю запрос на URL {API_URL}{resource}/{resource_id}'.format(
        API_URL=API_URL,
        resource=resource,
        resource_id=resource_id
    ))

    data = await get_json_response(
        API_URL,
        resource + '/' + str(resource_id)
    )

    # Трансформируем ключи из CamelCase в snake_case
    data = await from_camel_to_snake_json_keys(data)

    validated_data = pydantic_model(**data)

    return await db.create_obj(validated_data, resource=resource, telegram_user_id=telegram_user_id)


@custom_router.message(Command(commands=['get']), StateFilter(None))
async def get_command_handler(message: Message, state: State):
    logging.info('Вызываем обработчик `/get`')

    await message.answer(f'Отправляем запрос по URL {API_URL}\nКакой путь?', reply_markup=api_get_keyboard)

    # Устанавливаем состояние
    await state.set_state(APIResponseStates.which_resource)
    logging.info('Установлено состояние - WHICH_RESOURCE')

# -- Блок Callback Query хендлеров --

# Здесь функционал сводится к тому, что для каждого выбора пользователя появляется свой ответ
# и сохраняются необходимые данные. После этого одинаковый переход в следующее состояние - 'which_id'.
# Также предусмотрена кнопка отмены с отменой состояния.

@custom_router.callback_query(APIResponseStates.which_resource, F.data == 'users')
async def get_users_query_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выбран путь "/users".')
    logging.info('Вызываем обработчик `get_users_query_handler`')


    # Сохраняем ответ
    await state.update_data(resource='users', pydantic_model=UserModel)
    logging.info(f'Получено значение "users". Состояние - WHICH_RESOURCE')

    # Устанавливаем след. состояние
    await state.set_state(APIResponseStates.which_id)

    await callback.message.answer(
        f'Какой id ресурса?\nВведите целое число от 1 до {available_resources["users"]}.',
        reply_markup=back_and_cancel_keyboard
    )

@custom_router.callback_query(APIResponseStates.which_resource, F.data == 'posts')
async def get_posts_query_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выбран путь "/posts".')
    logging.info('Вызываем обработчик `get_posts_query_handler`')


    # Сохраняем ответ
    await state.update_data(resource='posts', pydantic_model=PostModel)
    logging.info(f'Получено значение "posts". Состояние - WHICH_RESOURCE')

    # Устанавливаем след. состояние
    await state.set_state(APIResponseStates.which_id)

    await callback.message.answer(
        f'Какой id ресурса?\nВведите целое число от 1 до {available_resources["posts"]}.',
        reply_markup=back_and_cancel_keyboard
    )


@custom_router.callback_query(APIResponseStates.which_resource, F.data == 'comments')
async def get_comments_query_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выбран путь "/comments".')
    logging.info('Вызываем обработчик `get_comments_query_handler`')


    # Сохраняем ответ
    await state.update_data(resource='comments', pydantic_model=CommentModel)
    logging.info(f'Получено значение "comments". Состояние - WHICH_RESOURCE')

    # Устанавливаем след. состояние
    await state.set_state(APIResponseStates.which_id)

    await callback.message.answer(
        f'Выбран путь "/comments". Какой id ресурса?\nВведите целое число от 1 до {available_resources["comments"]}.',
        reply_markup=back_and_cancel_keyboard
    )


@custom_router.callback_query(APIResponseStates.which_resource, F.data == 'albums')
async def get_albums_query_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выбран путь "/albums".')
    logging.info('Вызываем обработчик `get_albums_query_handler`')

    # Сохраняем ответ
    await state.update_data(resource='albums', pydantic_model=AlbumModel)
    logging.info(f'Получено значение "albums". Состояние - WHICH_RESOURCE')

    # Устанавливаем след. состояние
    await state.set_state(APIResponseStates.which_id)

    await callback.message.answer(
        f'Выбран путь "/albums". Какой id ресурса?\nВведите целое число от 1 до {available_resources["albums"]}.',
        reply_markup=back_and_cancel_keyboard
    )


@custom_router.callback_query(APIResponseStates.which_resource, F.data == 'photos')
async def get_photos_query_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выбран путь "/photos".')
    logging.info('Вызываем обработчик `get_photos_query_handler`')


    # Сохраняем ответ
    await state.update_data(resource='photos', pydantic_model=PhotoModel)
    logging.info(f'Получено значение "photos". Состояние - WHICH_RESOURCE')

    # Устанавливаем след. состояние
    await state.set_state(APIResponseStates.which_id)

    await callback.message.answer(
        f'Выбран путь "/photos". Какой id ресурса?\nВведите целое число от 1 до {available_resources["photos"]}.',
        reply_markup=back_and_cancel_keyboard
    )


@custom_router.callback_query(APIResponseStates.which_resource, F.data == 'todos')
async def get_todos_query_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выбран путь "/todos".')
    logging.info('Вызываем обработчик `get_todos_query_handler`')


    # Сохраняем ответ
    await state.update_data(resource='todos', pydantic_model=TodoModel)
    logging.info(f'Получено значение "todos". Состояние - WHICH_RESOURCE')

    # Устанавливаем след. состояние
    await state.set_state(APIResponseStates.which_id)

    await callback.message.answer(
        f'Выбран путь "/todos". Какой id ресурса?\nВведите целое число от 1 до {available_resources["todos"]}.',
        reply_markup=back_and_cancel_keyboard
    )


@custom_router.callback_query(APIResponseStates.which_id, F.data == 'back')
async def get_back_operation_handler(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик на случай, если пользователь захочет вернуться назад и выбрать другой вариант.
    """

    await callback.answer('Можете выбрать снова.')

    # Устанавливаем предыдущее состояние
    await state.set_state(APIResponseStates.which_resource)

    await callback.message.answer(
        f'Отправляем запрос по URL {API_URL}\nКакой путь?',
        reply_markup=api_get_keyboard
    )


@custom_router.callback_query(
    StateFilter(APIResponseStates.which_resource, APIResponseStates.which_id),
    F.data == 'cancel'
)
async def get_cancel_operation_handler(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик на случай, если пользователь захочет отменить команду.
    """

    logging.info('Вызываем обработчик `get_cancel_operation_handler`')

    await callback.answer('Отменено.')

    await callback.message.answer('Отменяю..')

    # Очищаем состояние
    await state.clear()

    await callback.message.answer('Готово. Можете снова написать команду /get или любую другую(см. /help)')

# -- Конец блока Callback Query --


@custom_router.message(APIResponseStates.which_id, F.text.isdigit())
async def get_response_data_handler(message: Message, state: State, db):
    """
    Конечная функция-обработчик в цепочке /get.
    Вызывает функцию `_get_api_data_and_save()` для выполнения всех действий с API и БД.
    """

    data = await state.get_data()
    logging.info(f'Получено значение {message.text}. Состояние - WHICH_ID')

    # Проверяем, что пользователь не вылез за пределы допустимых id
    if 1 <= int(message.text) <= available_resources[data['resource']]:
        try:
            await message.answer('Отправляю запрос и собираю данные..')

            # Передаем данные в функцию для запроса к API и сохранения в БД.
            data_db = await _get_api_data_and_save(
                db=db,
                pydantic_model=data['pydantic_model'],
                telegram_user_id=message.from_user.id,
                resource=data['resource'],
                resource_id=int(message.text)
            )

            await message.answer(f'Было получен и сохранен в БД ответ JSON:\n{data_db}')

            # Очищаем состояние
            await state.clear()

            await message.answer('Готово. Можете снова написать команду /get или любую другую(см. /help)')


        except SQLAlchemyError as e:
            logging.error(f'Произошла ошибка при при сохранении в БД:\n{e}')
            await message.answer('Какая-то ошибка при сохранении в БД, проверьте логи')

        except Exception as e:
            logging.error(f'Произошла ошибка при запросе:\n{e}')
            await message.answer('Произошла ошибка при запросе, проверьте логи')

    else:
        await message.answer(
            f'Было введено неверное число.\nПожалуйста, введите число от 1 до {available_resources[data["resource"]]}'
        )
