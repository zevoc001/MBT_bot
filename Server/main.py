import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from Server.handlers.handler import router as main_router
from Server.handlers.registrtion import router as reg_router
from Server.handlers.orders import router as order_router
from Server.handlers.menu_admin import router as admin_router

from middleware import AccessMiddleware


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(main_router)
    dp.include_router(reg_router)
    dp.include_router(order_router)
    dp.include_router(admin_router)

    dp.update.middleware(AccessMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutdown')
