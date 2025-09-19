from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
from config import API_ID, API_HASH, SESSION_NAME, REACTION, CHANNELS
from logger_setup import setup_logger

logger = setup_logger()
# Используем сессию из volume
session_path = f"sessions/{SESSION_NAME}"
app = Client(session_path, API_ID, API_HASH)


@app.on_message(filters.chat(CHANNELS))
async def react(client, message):
    try:
        await client.send_reaction(message.chat.id, message.id, REACTION)
        logger.info(
            f"Реакция {REACTION} добавлена в канал '{message.chat.title}' "
            f"на сообщение #{message.id} ({message.date.strftime('%Y-%m-%d %H:%M:%S')})"
        )
    except FloodWait as e:
        logger.warning(f"Превышен лимит FloodWait, ждем {e.x} секунд")
        await asyncio.sleep(e.x)
    except Exception as e:
        logger.error(f"Ошибка при добавлении реакции: {e}")
