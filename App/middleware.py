from aiogram import BaseMiddleware
from aiogram.types import Update, CallbackQuery
from typing import Callable, Any, Awaitable, Tuple
import database as db
import admin


async def get_access(user_id: int) -> tuple[str, str]:
    try:
        user = await db.get_user(user_id)
        user_access = user['access']
        user_status = user['status']
        return user_access, user_status
    except Exception as e:
        raise e


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
            try:
                if callback.data in admin.admin_command:
                    user_access, user_status = await get_access(user_id)
                    if user_access != 'admin' or user_status == 'blocked':
                        await callback.message.answer("У вас недостаточно прав для выполнения этого запроса.")
                        return
            except Exception as e:
                await callback.message.answer("Произошла ошибка при проверке ваших прав доступа.")
                return
        return await handler(event, data)
