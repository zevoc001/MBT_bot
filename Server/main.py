import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handler import router as main_router
from registrtion import router as reg_router
from orders import router as order_router
from menu_admin import router as admin_router

from middleware import AccessMiddleware


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(main_router)
    dp.include_router(reg_router)
    dp.include_router(order_router)
    dp.include_router(admin_router)

    dp.update.middleware(AccessMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutdown')
