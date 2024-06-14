import logging

import aiohttp
from datetime import date
from config import DB_URL, DB_ACCESS_TOKEN
from pydantic import BaseModel
from typing import Optional
import json
import os


async def get_data(url: str, params: dict = None):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': DB_ACCESS_TOKEN}
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()  # предполагается, что API возвращает JSON
                    return data
                else:
                    error_message = f"Failed to fetch data from {url}. Status code: {response.status}"
                    raise Exception(error_message)
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
            print(f"HTTP Client Error: {e}")
            return {}
        except json.JSONDecodeError:
            # Обработка ошибок при декодировании JSON
            print("Error decoding JSON from response")
            return {}
        except Exception as e:
            # Обработка других возможных ошибок
            print(f"An error occurred: {e}")
            return {}


async def put_data(url: str, data: dict = None, params: dict = None) -> dict:
    headers = {'Authorization': DB_ACCESS_TOKEN}
    async with aiohttp.ClientSession() as session:
        try:
            # Печатаем JSON-представление данных для отладки (при необходимости)
            # Отправка POST запроса
            async with session.put(url, json=data, params=params, headers=headers) as response:
                # Проверяем статус ответа
                response.raise_for_status()
                # Получаем и возвращаем JSON из ответа
                result_data = await response.json()
                return result_data
        except aiohttp.ClientError as e:
            # Обработка ошибок, связанных с сетью или HTTP
            print(f"HTTP Client Error: {e}")
            return {}
        except json.JSONDecodeError:
            # Обработка ошибок при декодировании JSON
            print("Error decoding JSON from response")
            return {}
        except Exception as e:
            # Обработка других возможных ошибок
            print(f"An error occurred: {e}")
            return {}


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
            print(f"HTTP Client Error: {e}")
            return {}
        except json.JSONDecodeError:
            # Обработка ошибок при декодировании JSON
            print("Error decoding JSON from response")
            return {}
        except Exception as e:
            # Обработка других возможных ошибок
            print(f"An error occurred: {e}")
            return {}


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
    result = await get_data(url)
    return result


async def get_users_by_name(pattern: str) -> dict:
    url = f'{DB_URL}/api/users/name/'
    params = {'pattern': pattern}
    result = await get_data(url, params)
    return result


async def get_user(user_id: int) -> dict:
    url = f'{DB_URL}/api/users/{user_id}'
    try:
        result = await get_data(url)
    except Exception as e:
        raise e
    return result


async def add_user(user: dict) -> dict:
    url = f'{DB_URL}/api/users/'
    result = await post_data(url, user)
    return result


async def update_user(user: dict) -> dict:
    url = f"{DB_URL}/api/users/"
    result = await put_data(url, user)
    return result


async def delete_user(user_id: int) -> dict:
    url = f"{DB_URL}/api/users/{user_id}"
    result = await delete_data(url)
    return result


# Employers
async def get_employers_all() -> list:
    url = f'{DB_URL}/api/employers/'
    result = await get_data(url)
    return result


async def get_employers_by_name(pattern: str) -> dict:
    url = f'{DB_URL}/api/employers/name/'
    params = {'pattern': pattern}
    result = await get_data(url, params)
    return result


async def get_employer(employer_id) -> dict:
    url = f'{DB_URL}/api/employers/{employer_id}'
    result = await get_data(url)
    return result


async def add_employer(employer: dict):
    url = f"{DB_URL}/api/employers/"
    result = await post_data(url, employer)
    return result


async def update_employer(employer_id: int, employer: dict):
    url = f"{DB_URL}/api/employers/"
    params = {'employer_id': employer_id}
    result = await put_data(url, employer, params)
    return result


async def delete_employer(employer_id: int):
    url = f"{DB_URL}/api/employers/{employer_id}"
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


async def add_order(order: dict) -> dict:
    url = f'{DB_URL}/api/orders/'
    result = await post_data(url, order)
    return result


async def update_order(order_id: int, order: dict):
    url = f'{DB_URL}/api/orders/{order_id}'
    result = await put_data(url, order)
    return result


async def finish_order(order_id: int):
    url = f'{DB_URL}/api/orders/status/'
    params = {'order_id': order_id}
    result = await put_data(url, params=params)
    return result


async def order_add_worker(order_id: int, worker_id: int):
    order = await get_order(order_id)  # Данные заказа
    workers = {column: value for column, value in order.items() if
               column.startswith('worker_telegram_id_')}  # таблица рабочих

    # Записан ли уже пользователь
    if worker_id in workers.values():
        raise KeyError('Пользователь уже записан')

    # Открыт ли заказ
    if order['status'] != 'Active':
        raise IndexError('К сожалению, мест больше нет')

    # Добавление рабочего в заказ
    for worker in workers:
        if workers[worker] is None:  # Пуст ли столбец
            order[worker] = worker_id
            await update_order(order_id, order)
            break

    # Проверка заполнения заказа
    order = await get_order(order_id)  # Данные заказа
    worker_count = len({column: value for column, value in order.items() if value is not None and
                        column.startswith('worker_telegram_id_')})
    print(worker_count)
    if worker_count == order['need_workers']:
        order['status'] = 'Closed'
        await update_order(order_id, order)
    return


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
    url = f'{DB_URL}/api/orders/worker/'
    params = {'user_id': user_id}
    result = await get_data(url, params)
    return result


async def upload_photo(file_path: str) -> dict:
    url = f"{DB_URL}/api/photo/"
    headers = {
        'Authorization': DB_ACCESS_TOKEN
    }

    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            data = aiohttp.FormData()
            data.add_field('photo', file, filename=os.path.basename(file_path))

            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response_text = await response.text()
                    raise Exception(f"Error {response.status}: {response_text}")


async def download_photo(file_name: str) -> bytes:
    url = f"{DB_URL}/api/photo/{file_name}"
    headers = {
        'Authorization': DB_ACCESS_TOKEN
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.read()
            else:
                response_text = await response.text()
                raise Exception(f"Error {response.status}: {response_text}")
