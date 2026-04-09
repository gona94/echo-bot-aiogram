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
python bot.py
```

Остановка: `Ctrl+C` в терминале.

## Структура

| Файл / папка     | Назначение                          |
|------------------|-------------------------------------|
| `bot.py`         | Код бота                            |
| `requirements.txt` | Зависимости Python              |
| `.env`           | Секреты (в Git не попадает)         |
| `.gitignore`     | Что Git не отслеживает              |
| `venv/`          | Виртуальное окружение (не в Git)    |
