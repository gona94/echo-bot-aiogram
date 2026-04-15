"""Утилиты для обработки входящих сообщений."""


def is_text_message(text: str | None) -> bool:
    """Проверяет, что сообщение содержит текст."""
    return text is not None and text.strip() != ""


def parse_integer_text(text: str) -> int | None:
    """Пробует распознать целое число в тексте."""
    normalized_text = text.strip()
    if not normalized_text:
        return None

    if normalized_text[0] in {"+", "-"}:
        number_part = normalized_text[1:]
        if number_part.isdigit():
            return int(normalized_text)
        return None

    if normalized_text.isdigit():
        return int(normalized_text)

    return None
