import aiohttp
from datetime import date
from config import DB_URL
from pydantic import BaseModel


async def get_data(url: str, params: dict = None) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()  # предполагается, что API возвращает JSON
                return data
            else:
                return [{"error": "Failed to fetch data", "status_code": response.status}]


async def post_data(url: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            result_data = await response.json()  # предполагается, что API возвращает JSON
            return result_data


class UserInfo(BaseModel):
    id: int
    telegram_id: str
    access: str | None
    data_reg: date | None
    status: str | None
    rating: int | None
    profit: int | None
    offers: int | None
    comment: str | None
    name: str | None
    sex: str | None
    born: date | None
    age: int | None
    residence: str | None
    education: str | None
    course: int | None
    profession: str | None
    salary: int | None
    hard_work: bool | None
    mid_work: bool | None
    art_work: bool | None
    other_work: str | None
    tools: str | None
    language: str | None
    phone: str | None
    email: str | None
    citizenship: str | None
    wallet: str | None
    is_driver: bool | None
    transport: str | None
    is_military: bool | None
    other_info: str | None


async def get_all_users() -> list:
    users = await get_data(f'{DB_URL}/users/get_users_all')
    return users


async def get_user_by_tg(telegram_id: int) -> list:
    user = await get_data(f'{DB_URL}/users/get_user_by_telegram', params={'telegram_id': telegram_id})
    return user


async def add_user(user: dict) -> dict:
    user = await post_data(f'{DB_URL}/users/add_user', data=user)
    return user

