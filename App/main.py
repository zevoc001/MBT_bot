import asyncio
from logger_config import get_logger

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers.handlers import router as handlers_router
from handlers.registrtion import router as reg_router
from handlers.orders import router as order_router


from middleware import AccessMiddleware


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(handlers_router)
    dp.include_router(reg_router)
    dp.include_router(order_router)

    dp.update.middleware(AccessMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
