"""Сервис с бизнес-логикой эхо-бота."""

from src.bot.utils.message_utils import is_text_message, parse_integer_text


class EchoService:
    """Сервис, который формирует ответы для пользователя."""

    def build_start_message(self) -> str:
        """Текст приветствия для команды /start."""
        return (
            "Привет! Напиши любое сообщение — я повторю его текст. "
            "Для режима LLM отправь команду /chatgpt, для возврата — /echo. "
            "Список команд: /help."
        )

    def build_help_message(self) -> str:
        """Возвращает краткую справку по доступным командам."""
        return (
            "Доступные команды:\n"
            "/start — приветствие и быстрые подсказки\n"
            "/help — список возможностей\n"
            "/chatgpt — включить режим LLM через OpenRouter\n"
            "/echo — выключить режим LLM и вернуться в эхо\n\n"
            "Дополнительно:\n"
            "- При слишком частых сообщениях включается anti-spam.\n"
            "- Длинные ответы автоматически обрезаются под лимит Telegram.\n"
            "- Для погоды/курсов/новостей бот честно сообщает, что у него нет live-доступа."
        )

    def build_echo_message(self, text: str | None) -> str:
        """Возвращает текст-ответ для входящего сообщения."""
        if not is_text_message(text):
            return "Я пока умею повторять только текстовые сообщения."

        normalized_text = text.strip()
        parsed_number = parse_integer_text(normalized_text)
        if parsed_number is not None:
            return str(parsed_number + 1)

        return normalized_text
