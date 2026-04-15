"""Роутер с обработчиками Telegram-сообщений."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

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
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            start_text = echo_service.build_start_message()
        await message.answer(start_text)

    @router.message(Command("help"))
    async def cmd_help(message: Message) -> None:
        """Показывает пользователю список доступных команд и ограничений."""
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            help_text = echo_service.build_help_message()
        await message.answer(help_text)

    @router.message(Command("chatgpt"))
    async def cmd_chatgpt(message: Message) -> None:
        """Включает режим ChatGPT для текущего пользователя."""
        if message.from_user is None:
            return

        chat_mode_service.enable(message.from_user.id)
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            response_text = "Режим ChatGPT включен. Теперь я отвечаю как LLM через OpenRouter."
        await message.answer(response_text)

    @router.message(Command("echo"))
    async def cmd_echo(message: Message) -> None:
        """Выключает режим ChatGPT и возвращает обычный эхо-режим."""
        if message.from_user is None:
            return

        chat_mode_service.disable(message.from_user.id)
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            response_text = "Режим ChatGPT выключен. Снова работаю как обычный эхо-бот."
        await message.answer(response_text)

    @router.message()
    async def echo_all(message: Message) -> None:
        """Ответ на любое входящее сообщение."""
        if message.from_user and not rate_limit_service.is_allowed(message.from_user.id):
            await message.answer("Слишком часто. Подожди секунду и отправь сообщение снова.")
            return

        if message.from_user and chat_mode_service.is_enabled(message.from_user.id):
            # Отправляем typing сразу и поддерживаем его, пока ждем ответ LLM.
            await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
            async with ChatActionSender.typing(
                bot=message.bot,
                chat_id=message.chat.id,
                interval=2.0,
            ):
                llm_answer = await openrouter_service.ask(message.text or "")
            await message.answer(trim_for_telegram(llm_answer))
            return

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            echo_answer = echo_service.build_echo_message(message.text)
        await message.answer(echo_answer)

    return router
