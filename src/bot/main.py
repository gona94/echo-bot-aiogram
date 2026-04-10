"""Главная точка входа для запуска Telegram-бота."""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from src.bot.config import load_config
from src.bot.routers.echo import create_echo_router
from src.bot.services.echo_service import EchoService


async def main() -> None:
    """Инициализирует и запускает бота."""
    logging.basicConfig(level=logging.INFO)

    try:
        config = load_config()
    except ValueError as exc:
        print(f"Ошибка конфигурации: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    bot = Bot(token=config.bot_token)
    dispatcher = Dispatcher()

    echo_service = EchoService()
    dispatcher.include_router(create_echo_router(echo_service))

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
