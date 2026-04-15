"""Тесты для сервиса эхо-бота."""

from src.bot.services.echo_service import EchoService


def test_build_start_message_returns_expected_text() -> None:
    """Проверяет корректный текст приветствия."""
    service = EchoService()
    result = service.build_start_message()

    assert (
        result
        == "Привет! Напиши любое сообщение — я повторю его текст. Для режима LLM отправь команду /chatgpt, для возврата — /echo."
    )


def test_build_echo_message_returns_trimmed_text() -> None:
    """Проверяет, что сервис возвращает обрезанный текст."""
    service = EchoService()
    result = service.build_echo_message("  Привет мир  ")

    assert result == "Привет мир"


def test_build_echo_message_for_non_text_returns_fallback() -> None:
    """Проверяет ответ, если пришло не текстовое сообщение."""
    service = EchoService()
    result = service.build_echo_message(None)

    assert result == "Я пока умею повторять только текстовые сообщения."


def test_build_echo_message_for_integer_returns_number_plus_one() -> None:
    """Если пришло число, сервис должен вернуть число + 1."""
    service = EchoService()
    result = service.build_echo_message("41")

    assert result == "42"


def test_build_echo_message_for_negative_integer_returns_number_plus_one() -> None:
    """Проверяет работу правила для отрицательного числа."""
    service = EchoService()
    result = service.build_echo_message("-2")

    assert result == "-1"
