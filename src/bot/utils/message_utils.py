"""Утилиты для обработки входящих сообщений."""


def is_text_message(text: str | None) -> bool:
    """Проверяет, что сообщение содержит текст."""
    return text is not None and text.strip() != ""
