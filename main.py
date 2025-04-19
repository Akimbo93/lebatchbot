import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from threading import Thread
from flask import Flask
from parser import checkfresh_parser  # импорт нашего парсера

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_TOKEN_HERE')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Заглушка Flask для Render / Ping
app = Flask(__name__)

@app.route('/')
def index():
    return "LeBatch is alive"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("👃 Привет! Я LeBatch — нюхач, проверяющий батч-коды. Напиши мне батч-код, и я скажу, когда аромат родился.")

@dp.message_handler()
async def handle_batch(message: types.Message):
    code = message.text.strip().upper()
    await message.answer("🔍 Проверяю батч-код...")

    # Пока принудительно бренд Chanel — дальше сделаем автоопределение
    brand = "chanel"
    result = checkfresh_parser(brand, code)

    if result["status"] == "ok":
        await message.answer(f"✅ Найдено:\n\n{result['result']}")
    elif result["status"] == "not_found":
        await message.answer("❓ Не удалось определить дату по этому батчу.")
    else:
        await message.answer(f"⚠️ Ошибка при запросе:\n{result['result']}")

if __name__ == '__main__':
    Thread(target=run_flask).start()
    executor.start_polling(dp, skip_updates=True)
