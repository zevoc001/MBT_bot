import datetime
import json
import os
from datetime import date
from typing import Optional

import aiohttp
from pydantic import BaseModel

from App.logger_config import get_logger
from config import DB_URL, DB_ACCESS_TOKEN
from dateutil.relativedelta import relativedelta

logger = get_logger(__name__)


class PageNotFound(BaseException):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'PageNotFound, {self.message}'
        else:
            return 'PageNotFound'


class UpdatingError(BaseException):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'UpdatingError, {self.message}'
        else:
            return 'UpdatingError'


class UserNotFound(BaseException):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'UserNotFound, {self.message}'
        else:
            return 'UserNotFound'


async def get_data(url: str, params: dict = None):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': DB_ACCESS_TOKEN}
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()  # предполагается, что API возвращает JSON
                    return data
                elif response.status == 404:
                    error_message = f"Failed to fetch data from {url}. Status code: {response.status}"
                    raise PageNotFound(error_message)
    except aiohttp.ClientError as e:
        # Handle network-related errors
        error_message = f"Error during HTTP request: {str(e)}"
        raise Exception(error_message)


async def post_data(url: str, data: dict, params: dict = None) -> dict:
    # Создание клиентской сессии
    async with aiohttp.ClientSession() as session:
        try:
            # Печатаем JSON-представление данных для отладки (при необходимости)
            # Отправка POST запроса
            async with session.post(url, json=data, params=params,
                                    headers={'Authorization': DB_ACCESS_TOKEN}) as response:
                # Проверяем статус ответа
                response.raise_for_status()
                # Получаем и возвращаем JSON из ответа
                result_data = await response.json()
                return result_data
        except aiohttp.ClientError as e:
            # Обработка ошибок, связанных с сетью или HTTP
            logger.error(f"HTTP Client Error: {e}")
            raise Exception(f'Ошибка сети: {e}')
        except json.JSONDecodeError as e:
            # Обработка ошибок при декодировании JSON
            logger.error(f"Ошибка обработки JSON: {e}")
            raise Exception(f'Ошибка обработки JSON: {e}')
        except Exception as e:
            # Обработка других возможных ошибок
            logger.error(f"Неизвестная ошибка: {e}")
            raise Exception(f'Неизвестная ошибка: {e}')


async def put_data(url: str, data: dict = None, params: dict = None) -> dict:
    headers = {'Authorization': DB_ACCESS_TOKEN}
    async with aiohttp.ClientSession() as session:
        try:
            # Печатаем JSON-представление данных для отладки (при необходимости)
            # Отправка POST запроса
            async with session.put(url, json=data, params=params, headers=headers) as response:
                # Проверяем статус ответа
                if response.status == 200:
                    # Получаем и возвращаем JSON из ответа
                    result_data = await response.json()
                    return result_data
                elif response.status == 422:
                    raise UpdatingError
                else:
                    raise Exception
        except aiohttp.ClientError as e:
            # Обработка ошибок, связанных с сетью или HTTP
            logger.error(f'Ошибка сети: {e}')
            raise Exception(f'Ошибка сети: {e}')
        except json.JSONDecodeError as e:
            # Обработка ошибок при декодировании JSON
            logger.error(f'Ошибка обработки JSON: {e}')
            raise Exception(f'Ошибка обработки JSON: {e}')
        except Exception as e:
            # Обработка других возможных ошибок
            logger.error(f"Неизвестная ошибка: {e}")
            raise Exception(f'Неизвестная ошибка: {e}')


async def delete_data(url: str, params: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            # Печатаем JSON-представление данных для отладки (при необходимости)
            # Отправка POST запроса
            async with session.delete(url, params=params, headers={'Authorization': DB_ACCESS_TOKEN}) as response:
                # Проверяем статус ответа
                response.raise_for_status()
                # Получаем и возвращаем JSON из ответа
                result_data = await response.json()
                return result_data
        except aiohttp.ClientError as e:
            # Обработка ошибок, связанных с сетью или HTTP
            logger.error(f'Ошибка сети: {e}')
            raise Exception(f'Ошибка сети: {e}')
        except json.JSONDecodeError as e:
            # Обработка ошибок при декодировании JSON
            print("Error decoding JSON from response")
            raise Exception(f'Ошибка обработки JSON: {e}')
        except Exception as e:
            # Обработка других возможных ошибок
            print(f"An error occurred: {e}")
            raise Exception(f'Неизвестная ошибка: {e}')


class UserInfo(BaseModel):
    id: Optional[str] = None
    access: Optional[str] = None
    reg_date: date
    status: Optional[str] = None
    rating: Optional[int] = None
    profit: Optional[int] = None
    offers: Optional[int] = None
    comment: Optional[int] = None
    name: Optional[str] = None
    sex: Optional[str] = None
    born_date: Optional[date] = None
    residence: Optional[str] = None
    education: Optional[str] = None
    course: Optional[int] = None
    profession: Optional[str] = None
    salary: Optional[int] = None
    hard_work: Optional[bool] = None
    mid_work: Optional[bool] = None
    art_work: Optional[bool] = None
    other_work: Optional[str] = None
    tools: Optional[str] = None
    language: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    citizenship: Optional[str] = None
    wallet: Optional[str] = None
    is_driver: Optional[bool] = None
    transport: Optional[str] = None
    is_military: Optional[bool] = None
    other_info: Optional[str] = None


# Users
async def get_users_all() -> list:
    url = f'{DB_URL}/api/users/'
    try:
        return await get_data(url)
    except Exception as e:
        raise Exception(f'Ошибка запроса: {e}')


async def get_users_by_name(pattern: str) -> dict:
    url = f'{DB_URL}/api/users/name/'
    try:
        params = {'pattern': pattern}
        return await get_data(url, params)
    except Exception as e:
        raise Exception(f'Ошибка запроса: {e}')


async def get_users_by_sex(sex: str) -> dict:
    url = f'{DB_URL}/api/users/sex/'
    if sex in ['Мужской', 'Женский']:
        params = {'sex': sex}
        try:
            return await get_data(url, params)
        except Exception as e:
            raise Exception(f'Ошибка запроса: {e}')
    else:
        raise Exception('Неверный ввод')


async def get_users_by_age(age: int, sign: str) -> dict:
    url = f'{DB_URL}/api/users/born_date/'
    today = datetime.date.today()
    if sign == '>':
        date_from = datetime.date(1, 1, 1)
        date_to = today - relativedelta(years=age)
    else:
        date_from = today - relativedelta(years=age)
        date_to = today
    params = {
        'date_from': date_from.isoformat(),
        'date_to': date_to.isoformat(),
    }
    try:
        return await get_data(url, params)
    except Exception as e:
        raise Exception(f'Не удалось найти пользователя по дате рождения: {e}')


async def get_user(user_id: int) -> dict:
    url = f'{DB_URL}/api/users/{user_id}'
    try:
        result = await get_data(url)
        return result
    except PageNotFound:
        raise UserNotFound(f'Не удалось получить пользователя: {e}')
    except Exception as e:
        logger.warning(f'Не удалось получить пользователя: {e}')
        raise e


async def add_user(user: dict) -> dict:
    url = f'{DB_URL}/api/users/'
    result = await post_data(url, user)
    return result


async def update_user(user: dict) -> dict:
    url = f"{DB_URL}/api/users/"
    params = {'user_id': user['id']}
    try:
        result = await put_data(url=url, params=params, data=user)
        return result
    except UpdatingError:
        raise UserNotFound
    except Exception:
        raise UpdatingError


async def delete_user(user_id: int) -> dict:
    url = f"{DB_URL}/api/users/{user_id}"
    result = await delete_data(url)
    return result


# Employers
async def get_customers_all() -> list:
    url = f'{DB_URL}/api/customers/'
    result = await get_data(url)
    return result


async def get_customers_by_name(pattern: str) -> dict:
    url = f'{DB_URL}/api/customers/name/'
    params = {'pattern': pattern}
    result = await get_data(url, params)
    return result


async def get_customers(customer_id) -> dict:
    url = f'{DB_URL}/api/customers/{customer_id}'
    result = await get_data(url)
    return result


async def add_customers(customer: dict):
    url = f"{DB_URL}/api/customers/"
    result = await post_data(url, customer)
    return result


async def update_customer(customer_id: int, customer: dict):
    url = f"{DB_URL}/api/customers/"
    params = {'customers_id': customer_id}
    result = await put_data(url, customer, params)
    return result


async def delete_customers(customer_id: int):
    url = f"{DB_URL}/api/customers/{customer_id}"
    result = await delete_data(url)
    return result


#Orders
async def get_orders_all() -> list:
    url = f'{DB_URL}/api/orders/'
    result = await get_data(url)
    return result


async def get_order(order_id) -> dict:
    url = f'{DB_URL}/api/orders/{order_id}'
    result = await get_data(url)
    return result


async def get_order_workers(order_id) -> list:
    url = f'{DB_URL}/api/orders/{order_id}/workers_id'
    result = await get_data(url)
    return result


async def add_order(order: dict) -> dict:
    url = f'{DB_URL}/api/orders/'
    result = await post_data(url, order)
    return result


async def update_order(order_id: int, order: dict):
    """
    Обновляет данные заказа
    :param order_id: Номер заказа
    :param order: Новые данные заказа
    :return:
    """
    url = f'{DB_URL}/api/orders/{order_id}'
    try:
        await put_data(url, order)
    except Exception as e:
        logger.error(f'Не удалось обновить данные заказа: {e}')
        raise e


async def order_add_worker(order_id: int, worker_id: int):
    url = f'{DB_URL}/api/orders/{order_id}/workers/'
    data = {
        'worker_id': worker_id
    }
    try:
        await post_data(url, data=data)
    except Exception as e:
        logger.error(f'Не удалось добавить рабочего в заказ: {e}')
        raise e


async def order_remove_worker(order_id: int, worker_id: int):
    order = await get_order(order_id)
    workers = {column: value for column, value in order.items() if
               column.startswith('worker_telegram_id_')}

    for worker in workers:
        if workers[worker] == worker_id:  # Пуст ли столбец
            order[worker] = None
            if order['status'] == 'Closed':
                order['status'] = 'Active'
                await update_order(order_id, order)
                break
    return


async def get_users_orders(user_id):
    url = f'{DB_URL}/api/users/{user_id}/orders/'
    result = await get_data(url)
    return result
