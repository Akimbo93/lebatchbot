import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode

API_TOKEN = 'YOUR_TOKEN_HERE'  # <-- Вставь свой токен сюда
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("👃 Привет! Я LeBatch — нюхач, проверяющий батч-коды. Напиши мне батч-код, и я скажу, когда аромат родился.")

@dp.message_handler()
async def handle_batch(message: types.Message):
    text = message.text.strip().upper()
    await message.answer("🔍 Проверяю батч-код...")

    result = check_batch_code(text)
    await message.answer(result, parse_mode=ParseMode.MARKDOWN)

def check_batch_code(code):
    # Пример заглушки
    fake_data = {
        "38R103W": "*Dior Sauvage EDP*
📅 Дата производства: Октябрь 2023
🏭 Завод: Франция
✅ Свежий, бери смело!",
        "8X01": "*Chanel Bleu EDP*
📅 Дата производства: Июль 2022
⚠️ Может быть уже не в лучшей форме, нюхай сам."
    }
    return fake_data.get(code, "❓ Не нашёл этот батч в базе. Возможно, бренд не поддерживается.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
