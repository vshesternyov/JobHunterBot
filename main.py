import os
import dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import register_handlers

dotenv.load_dotenv()

bot_token = os.environ.get('TOKEN')

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_handlers(dp)

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
