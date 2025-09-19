# Telegram Reaction Bot

Автоматический Telegram-бот, который ставит реакции на новые сообщения в указанных каналах.
Проект полностью контейнеризирован с помощью Docker и Docker Compose, что позволяет запускать бота на любой машине с установленным Docker.

---

## ⚙️ Возможности

- Автоматическая установка реакции на новые сообщения.
- Поддержка нескольких каналов.
- Логи с ротацией (1 МБ, 3 резервные копии).
- Работа через Docker и Docker Compose.
- Безопасное хранение конфиденциальных данных через `.env`.

---

## 📝 Требования

- Python 3.13+
- Docker
- Docker Compose
- Telegram API ID и API HASH
- Pyrogram

---

## 📦 Установка и запуск

1. Клонируем репозиторий:

```
git clone https://github.com/yudenkodanil/telegram-reaction.git
cd telegram-reaction
mv .env.example .env
nano .env

```

2. Настраиваем файл `.env` на основе шаблона `.env.example` и заполняем данные:

```
API_ID=ваш_api_id
API_HASH=ваш_api_hash
SESSION_NAME=reaction_bot
REACTION=⚡️
CHANNELS= #название каналов через запятую
```

3. Запуск через Docker Compose:

```
docker compose up -d --build
```

4. Проверка логов:

```
docker-compose logs -f
```

> Логи также сохраняются на хосте, если настроен volume в `docker-compose.yml`.

---

## 📁 Структура проекта

```
telegram_reaction_bot/
├─ main.py               # Точка входа бота
├─ bot_handler.py        # Основная логика работы с Pyrogram
├─ config.py             # Загрузка конфигурации из .env
├─ logger_setup.py       # Настройка логирования
├─ requirements.txt      # Python зависимости
├─ .env.example          # Шаблон конфигурации
├─ Dockerfile
└─ docker-compose.yml
```

---

## 🔒 Безопасность

- Реальные `.env` файлы и сессии Pyrogram не включены в репозиторий.
- Логи и файлы сессий игнорируются через `.gitignore`.

---

## ⚡ Использование

- Настроить файл `.env`.


---

## 📄 Лицензия

MIT License
