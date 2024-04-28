import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router as main_router
from registrtion import router as reg_router
from aiogram.fsm.storage.memory import MemoryStorage

ADMIN_ID = "1383046637"  # ID админа


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)
    dp.include_router(reg_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
