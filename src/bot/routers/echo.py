"""Роутер с обработчиками Telegram-сообщений."""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.bot.services.echo_service import EchoService


def create_echo_router(echo_service: EchoService) -> Router:
    """Создает роутер и подключает обработчики с внедренным сервисом."""
    router = Router()

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        """Ответ на команду /start."""
        await message.answer(echo_service.build_start_message())

    @router.message()
    async def echo_all(message: Message) -> None:
        """Ответ на любое входящее сообщение."""
        await message.answer(echo_service.build_echo_message(message.text))

    return router
