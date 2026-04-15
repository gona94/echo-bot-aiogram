"""Сервис хранения режима диалога пользователя."""


class ChatModeService:
    """Управляет включением и проверкой режима ChatGPT для пользователя."""

    def __init__(self) -> None:
        self._enabled_user_ids: set[int] = set()

    def enable(self, user_id: int) -> None:
        """Включает режим ChatGPT для пользователя."""
        self._enabled_user_ids.add(user_id)

    def disable(self, user_id: int) -> None:
        """Выключает режим ChatGPT для пользователя."""
        self._enabled_user_ids.discard(user_id)

    def is_enabled(self, user_id: int) -> bool:
        """Проверяет, включен ли режим ChatGPT для пользователя."""
        return user_id in self._enabled_user_ids
