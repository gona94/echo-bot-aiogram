"""Сервис с бизнес-логикой эхо-бота."""

from src.bot.utils.message_utils import is_text_message


class EchoService:
    """Сервис, который формирует ответы для пользователя."""

    def build_start_message(self) -> str:
        """Текст приветствия для команды /start."""
        return "Привет! Напиши любое сообщение — я повторю его текст."

    def build_echo_message(self, text: str | None) -> str:
        """Возвращает текст-ответ для входящего сообщения."""
        if not is_text_message(text):
            return "Я пока умею повторять только текстовые сообщения."
        return text.strip()
