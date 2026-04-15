"""Роутер с обработчиками Telegram-сообщений."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from src.bot.services.chat_mode_service import ChatModeService
from src.bot.services.echo_service import EchoService
from src.bot.services.openrouter_service import OpenRouterService
from src.bot.services.rate_limit_service import RateLimitService
from src.bot.utils.telegram_text_utils import trim_for_telegram


def create_echo_router(
    echo_service: EchoService,
    chat_mode_service: ChatModeService,
    openrouter_service: OpenRouterService,
    rate_limit_service: RateLimitService,
) -> Router:
    """Создает роутер и подключает обработчики с внедренным сервисом."""
    router = Router()

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        """Ответ на команду /start."""
        await message.answer(echo_service.build_start_message())

    @router.message(Command("help"))
    async def cmd_help(message: Message) -> None:
        """Показывает пользователю список доступных команд и ограничений."""
        await message.answer(echo_service.build_help_message())

    @router.message(Command("chatgpt"))
    async def cmd_chatgpt(message: Message) -> None:
        """Включает режим ChatGPT для текущего пользователя."""
        if message.from_user is None:
            return

        chat_mode_service.enable(message.from_user.id)
        await message.answer(
            "Режим ChatGPT включен. Теперь я отвечаю как LLM через OpenRouter."
        )

    @router.message(Command("echo"))
    async def cmd_echo(message: Message) -> None:
        """Выключает режим ChatGPT и возвращает обычный эхо-режим."""
        if message.from_user is None:
            return

        chat_mode_service.disable(message.from_user.id)
        await message.answer("Режим ChatGPT выключен. Снова работаю как обычный эхо-бот.")

    @router.message()
    async def echo_all(message: Message) -> None:
        """Ответ на любое входящее сообщение."""
        if message.from_user and not rate_limit_service.is_allowed(message.from_user.id):
            await message.answer("Слишком часто. Подожди секунду и отправь сообщение снова.")
            return

        if message.from_user and chat_mode_service.is_enabled(message.from_user.id):
            llm_answer = await openrouter_service.ask(message.text or "")
            await message.answer(trim_for_telegram(llm_answer))
            return

        await message.answer(echo_service.build_echo_message(message.text))

    return router
