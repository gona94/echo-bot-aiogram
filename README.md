# Эхо-бот на Python (aiogram)

Бот повторяет текст ваших сообщений. Токен хранится в `.env` и **не** коммитится в Git.

## Требования

- Python 3.10 или новее
- Аккаунт Telegram и токен бота от [@BotFather](https://t.me/BotFather)

## Настройка

1. Клонируйте или скачайте проект.
2. Создайте виртуальное окружение и установите зависимости.

### Windows (PowerShell)

```powershell
cd "путь\к\проекту"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Если выполнение скриптов запрещено политикой, один раз выполните:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### macOS / Linux

```bash
cd /path/to/project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. В корне проекта отредактируйте файл `.env`:

```env
BOT_TOKEN=ваш_реальный_токен
```

## Запуск

С активированным виртуальным окружением:

```bash
python -m src.bot.main
```

Остановка: `Ctrl+C` в терминале.

Альтернативно (для совместимости) можно запускать и так:

```bash
python bot.py
```

## Правила работы с секретами

- Храните токены и ключи только в локальных файлах (`.env`, локальный `mcp.json`), не в коде.
- Никогда не коммитьте секреты в Git и не вставляйте их в `README.md`.
- Не отправляйте ключи в чаты, на скриншоты и в публичные материалы.
- При подозрении на утечку сразу перевыпускайте ключ (Regenerate/Revoke).

Автоматическая защита перед коммитом:

```bash
git config core.hooksPath .githooks
```

После этой команды Git будет запускать `scripts/check_secrets.py` перед каждым коммитом.

## Структура

| Файл / папка              | Назначение                                      |
|---------------------------|-------------------------------------------------|
| `src/bot/main.py`         | Главная точка входа и запуск приложения         |
| `src/bot/config.py`       | Загрузка и валидация `.env`                     |
| `src/bot/routers/`        | Telegram-обработчики (только маршрутизация)     |
| `src/bot/services/`       | Бизнес-логика                                   |
| `src/bot/utils/`          | Вспомогательные функции                          |
| `bot.py`                  | Точка совместимости для старого запуска          |
| `requirements.txt`        | Зависимости Python                              |
| `.env`                    | Секреты (в Git не попадает)                     |
| `.gitignore`              | Что Git не отслеживает                          |
| `venv/`                   | Виртуальное окружение (не в Git)                |
