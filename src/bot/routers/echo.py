"""Роутер с обработчиками Telegram-сообщений."""

import asyncio
import contextlib
from typing import Awaitable, TypeVar

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from src.bot.services.chat_mode_service import ChatModeService
from src.bot.services.echo_service import EchoService
from src.bot.services.openrouter_service import OpenRouterService
from src.bot.services.rate_limit_service import RateLimitService
from src.bot.services.stale_message_service import StaleMessageService
from src.bot.utils.telegram_text_utils import trim_for_telegram

T = TypeVar("T")


def create_echo_router(
    echo_service: EchoService,
    chat_mode_service: ChatModeService,
    openrouter_service: OpenRouterService,
    rate_limit_service: RateLimitService,
    stale_message_service: StaleMessageService,
) -> Router:
    """Создает роутер и подключает обработчики с внедренным сервисом."""
    router = Router()

    async def _run_with_typing(message: Message, coro: Awaitable[T]) -> T:
        """Поддерживает индикатор typing, пока выполняется операция."""
        async def _typing_loop() -> None:
            while True:
                await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
                # Telegram показывает typing ограниченное время, поэтому обновляем регулярно.
                await asyncio.sleep(2.0)

        typing_task = asyncio.create_task(_typing_loop())
        try:
            # Короткая пауза дает клиенту шанс отрисовать индикатор до ответа.
            await asyncio.sleep(0.25)
            return await coro
        finally:
            typing_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await typing_task

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        """Ответ на команду /start."""
        if stale_message_service.is_stale(message.date):
            return
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            start_text = echo_service.build_start_message()
        await message.answer(start_text)

    @router.message(Command("help"))
    async def cmd_help(message: Message) -> None:
        """Показывает пользователю список доступных команд и ограничений."""
        if stale_message_service.is_stale(message.date):
            return
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            help_text = echo_service.build_help_message()
        await message.answer(help_text)

    @router.message(Command("chatgpt"))
    async def cmd_chatgpt(message: Message) -> None:
        """Включает режим ChatGPT для текущего пользователя."""
        if stale_message_service.is_stale(message.date):
            return
        if message.from_user is None:
            return

        chat_mode_service.enable(message.from_user.id)
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            response_text = "Режим ChatGPT включен. Теперь я отвечаю как LLM через OpenRouter."
        await message.answer(response_text)

    @router.message(Command("echo"))
    async def cmd_echo(message: Message) -> None:
        """Выключает режим ChatGPT и возвращает обычный эхо-режим."""
        if stale_message_service.is_stale(message.date):
            return
        if message.from_user is None:
            return

        chat_mode_service.disable(message.from_user.id)
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            response_text = "Режим ChatGPT выключен. Снова работаю как обычный эхо-бот."
        await message.answer(response_text)

    @router.message()
    async def echo_all(message: Message) -> None:
        """Ответ на любое входящее сообщение."""
        if stale_message_service.is_stale(message.date):
            return
        if message.from_user and not rate_limit_service.is_allowed(message.from_user.id):
            await message.answer("Слишком часто. Подожди секунду и отправь сообщение снова.")
            return

        if message.from_user and chat_mode_service.is_enabled(message.from_user.id):
            progress_message: Message | None = None
            try:
                progress_message = await message.answer("⏳ Думаю над ответом...")
            except TelegramBadRequest:
                # Если Telegram отклонил сообщение-индикатор, продолжаем без него.
                progress_message = None

            try:
                llm_answer = await _run_with_typing(
                    message,
                    openrouter_service.ask(message.text or ""),
                )
            finally:
                if progress_message is not None:
                    with contextlib.suppress(TelegramBadRequest):
                        await progress_message.delete()

            await message.answer(trim_for_telegram(llm_answer))
            return

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            echo_answer = echo_service.build_echo_message(message.text)
        await message.answer(echo_answer)

    return router
