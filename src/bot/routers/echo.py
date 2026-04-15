"""Роутер с обработчиками Telegram-сообщений."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from src.bot.services.chat_mode_service import ChatModeService
from src.bot.services.echo_service import EchoService
from src.bot.services.openrouter_service import OpenRouterService


def create_echo_router(
    echo_service: EchoService,
    chat_mode_service: ChatModeService,
    openrouter_service: OpenRouterService,
) -> Router:
    """Создает роутер и подключает обработчики с внедренным сервисом."""
    router = Router()

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        """Ответ на команду /start."""
        await message.answer(echo_service.build_start_message())

    @router.message(Command("chatgpt"))
    async def cmd_chatgpt(message: Message) -> None:
        """Включает режим ChatGPT для текущего пользователя."""
        if message.from_user is None:
            return

        chat_mode_service.enable(message.from_user.id)
        await message.answer(
            "Режим ChatGPT включен. Теперь я отвечаю как LLM через OpenRouter."
        )

    @router.message()
    async def echo_all(message: Message) -> None:
        """Ответ на любое входящее сообщение."""
        if message.from_user and chat_mode_service.is_enabled(message.from_user.id):
            llm_answer = await openrouter_service.ask(message.text or "")
            await message.answer(llm_answer)
            return

        await message.answer(echo_service.build_echo_message(message.text))

    return router
