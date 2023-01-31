from aiogram import Bot, Dispatcher, executor
import aiogram
import os
import resource
import psutil
import signal

import config

print(resource.welcome_text)
current_path = config.current_path
bot = Bot(config.token)
dp = Dispatcher(bot)
admin = 5806919527


@dp.message_handler()


if __name__ == '__main__':
    executor.start_polling(dp)