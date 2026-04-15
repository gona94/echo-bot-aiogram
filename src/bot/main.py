"""Главная точка входа для запуска Telegram-бота."""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from src.bot.config import load_config
from src.bot.routers.echo import create_echo_router
from src.bot.services.chat_mode_service import ChatModeService
from src.bot.services.echo_service import EchoService
from src.bot.services.openrouter_service import OpenRouterService
from src.bot.services.rate_limit_service import RateLimitService
from src.bot.services.stale_message_service import StaleMessageService


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
    chat_mode_service = ChatModeService()
    rate_limit_service = RateLimitService(min_interval_seconds=1.0)
    stale_message_service = StaleMessageService(max_age_seconds=20)
    openrouter_service = OpenRouterService(
        api_key=config.openrouter_api_key,
        model=config.openrouter_model,
    )
    dispatcher.include_router(
        create_echo_router(
            echo_service,
            chat_mode_service,
            openrouter_service,
            rate_limit_service,
            stale_message_service,
        )
    )

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
