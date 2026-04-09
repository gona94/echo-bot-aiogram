"""
Простой эхо-бот: повторяет текст сообщения пользователя.
Токен бота читается из переменной окружения BOT_TOKEN (файл .env).
"""

import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем переменные из файла .env в корне проекта
load_dotenv()

# Настраиваем простой вывод ошибок в консоль
logging.basicConfig(level=logging.INFO)


def get_bot_token() -> str:
    """Возвращает токен из окружения или пустую строку, если его нет."""
    token = os.getenv("BOT_TOKEN", "").strip()
    return token


async def main() -> None:
    token = get_bot_token()
    if not token:
        print(
            "Ошибка: не задан BOT_TOKEN.\n"
            "Создайте файл .env в корне проекта со строкой:\n"
            "BOT_TOKEN=ваш_токен_от_BotFather",
            file=sys.stderr,
        )
        sys.exit(1)

    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        """Ответ на команду /start."""
        await message.answer(
            "Привет! Напиши любое сообщение — я повторю его текст."
        )

    @dp.message()
    async def echo_all(message: Message) -> None:
        """Повторяем текст сообщения (эхо)."""
        # Если пришло не текст (стикер, фото и т.д.) — сообщаем об этом
        if message.text is None:
            await message.answer("Я пока умею повторять только текстовые сообщения.")
            return
        await message.answer(message.text)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
