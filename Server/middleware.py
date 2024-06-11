from aiogram import BaseMiddleware
from aiogram.types import Update, CallbackQuery

from typing import Callable, Any, Awaitable
import logging

from Server import database as db
from Server import admin


async def has_access(user_id: int, request: str) -> bool:
    user = await db.get_user(user_id)
    user_access = user['access']
    if request in admin.admin_command:
        return user_access == 'admin'
    else:
        return True


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict], Awaitable[Any]],
        event: Any,
        data: dict
    ) -> Any:
        if isinstance(event, Update) and event.callback_query:
            callback: CallbackQuery = event.callback_query
            user_id = callback.from_user.id
            request = callback.data
            logging.debug('Проверка прав')
            if not await has_access(user_id, request):
                await callback.message.answer("У вас недостаточно прав для выполнения этого запроса.")
                return
        return await handler(event, data)
