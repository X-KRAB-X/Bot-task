import logging
import json

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
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


async def _get_api_data(resource: str, resource_id: int, pydantic_model):
    """
    Функция для выполнения запросов к API и трансформации данных.

    :param resource: Название URL, по которому был отправлен запрос.
    :param resource_id: ID выбранного ресурса.
    :param pydantic_model: Pydantic-модель в зависимости от выбранного ресурса.

    :return: Pydantic-модель с данными внутри.
    """

    logging.info('Отправляю запрос на URL {API_URL}{resource}/{resource_id}'.format(
        API_URL=API_URL,
        resource=resource,
        resource_id=resource_id
    ))

    # Отправляем запрос
    data = await get_json_response(
        API_URL,
        resource + '/' + str(resource_id)
    )

    # Трансформируем ключи из CamelCase в snake_case
    data = await from_camel_to_snake_json_keys(data)

    validated_data = pydantic_model(**data)

    return validated_data


async def _save_data_into_db(db, validated_data, resource: str, telegram_user_id):
    """
    Функция-исполнитель для работы с БД.

    :param db: Сервис БД для сохранения объекта.
    :param validated_data: Pydantic-модель с данными.
    :param resource: Название метода, который необходимо вызвать для сохранения.
    Соответствует названию ресурса.
    :param telegram_user_id: ID пользователя.

    :return: JSON-Pydantic модель с данными из БД.
    """

    logging.info('Сохраняю данные в БД')
    return await db.create_obj(validated_data, resource=resource, telegram_user_id=telegram_user_id)


async def _save_data_into_gh(gh, validated_data, resource: str, telegram_user_id):
    """
    Функция-исполнитель для работы с Google Sheets.

    :param gh: Сервис Google Sheets для сохранения объекта.
    :param validated_data: Pydantic-модель с данными.
    :param resource: Название метода, который необходимо вызвать для сохранения.
    Соответствует названию ресурса.
    :param telegram_user_id: ID пользователя.
    """

    logging.info('Сохраняю данные в Google Sheets')
    await gh.create_obj(validated_data, resource=resource, telegram_user_id=telegram_user_id)
    logging.info('Успешно сохранены данные в Google Sheets')


@custom_router.message(Command(commands=['get']), StateFilter(None))
async def get_command_handler(message: Message, state: FSMContext):
    logging.info('Вызываем обработчик `/get`')

    await message.answer(f'Отправляем запрос по URL {API_URL}\nКакой путь?', reply_markup=api_get_keyboard)

    # Устанавливаем состояние
    await state.set_state(APIResponseStates.which_resource)
    logging.info('Установлено состояние - WHICH_RESOURCE')


# ~~~~~~~~~~~~~~~~~~~~~~~~~ Блок Callback-Query хендлеров ~~~~~~~~~~~~~~~~~~~~~~~~~

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
        f'Выбран путь "/users". Какой id ресурса?\nВведите целое число от 1 до {available_resources["users"]}.',
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
        f'Выбран путь "/posts". Какой id ресурса?\nВведите целое число от 1 до {available_resources["posts"]}.',
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
        f'Вы вернулись назад.\nОтправляем запрос по URL {API_URL}\nКакой путь?',
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Конец блока Callback Query ~~~~~~~~~~~~~~~~~~~~~~~~~


@custom_router.message(APIResponseStates.which_id, F.text.isdigit())
async def get_response_data_handler(message: Message, state: FSMContext, db, gh):
    """
    Конечная функция-обработчик в цепочке /get.

    Служит связующим звеном между данными и функциями-исполнителями.
    Вызывает функцию `_get_api_data`, после чего данные из нее
    передаются в функции `_save_data_into_gh` и `_save_data_into_db`.

    В конце чистит состояние.
    """

    data = await state.get_data()
    logging.info(f'Получено значение {message.text}. Состояние - WHICH_ID')

    # Проверяем, что пользователь не вылез за пределы допустимых id
    if 1 <= int(message.text) <= available_resources[data['resource']]:
        try:
            # Получаем данные API
            await message.answer('Отправляю запрос и собираю данные..')

            api_data = await _get_api_data(
                resource=data['resource'],
                resource_id=int(message.text),
                pydantic_model=data['pydantic_model']
            )
            await message.answer('Готово!')

            # Сохраняем данные в Google Sheets
            await message.answer('Сохраняю данные в Google Sheets..')

            await _save_data_into_gh(
                gh=gh,
                validated_data=api_data,
                resource=data['resource'],
                telegram_user_id=message.from_user.id
            )
            await message.answer('Готово!')

            # Сохраняем в PostgreSQL
            await message.answer('Сохраняю данные в БД..')

            db_data = await _save_data_into_db(
                db=db,
                validated_data=api_data,
                resource=data['resource'],
                telegram_user_id=message.from_user.id
            )
            await message.answer(f'Готово! Ответ БД в JSON-формате:\n{db_data}')

            # Очищаем состояние
            await state.clear()

            await message.answer(
                'Все готово. Можете снова написать команду /get или любую другую (см. /help)'
            )


        except SQLAlchemyError as e:
            logging.error(f'Произошла ошибка при при сохранении в БД:\n{e}')
            await message.answer('Какая-то ошибка при сохранении в БД, проверьте логи')

        except Exception as e:
            logging.error(f'Произошла непредвиденная ошибка:\n{e}')
            await message.answer('Произошла непредвиденная ошибка, проверьте логи')

    else:
        await message.answer(
            f'Было введено неверное число.\nПожалуйста, введите число от 1 до {available_resources[data["resource"]]}'
        )
