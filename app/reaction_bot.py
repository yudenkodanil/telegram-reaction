import os
import time
import asyncio
import random
from telethon import TelegramClient, events
from telethon.tl.types import ReactionEmoji
from telethon.tl.functions.messages import SendReactionRequest
from app.logger import logger
from app.config import Config
from datetime import datetime


class ReactionBot:
    def __init__(self):
        self.client = TelegramClient(
            Config.SESSION_FILE,
            Config.API_ID,
            Config.API_HASH
        )

    async def add_reaction(self, message, reaction: str) -> str:
        """
        Ставит реакцию и возвращает статус:
        'applied' — поставлена, 'skipped' — уже была, 'error' — ошибка.
        """
        try:
            channel_title = getattr(message.chat, "title", None) or str(getattr(message, "chat_id", None))
            msg_id = getattr(message, "id", None)
            date_obj = getattr(message, "date", None)
            date_formatted = date_obj.strftime("%d-%m-%Y %H:%M") if date_obj else "unknown"

            # проверяем, стоит ли уже реакция
            if getattr(message, "reactions", None) and getattr(message.reactions, "results", None):
                for r in message.reactions.results:
                    if getattr(r.reaction, "emoticon", None) == reaction and getattr(r, "chosen_order", None) is not None:
                        logger.debug("Пропущено: реакция уже есть на %s в канале \"%s\"", msg_id, channel_title)
                        return "skipped"

            peer = getattr(message, "chat_id", None) or getattr(message, "peer_id", None)
            # пытаемся high-level
            if hasattr(self.client, "send_reaction"):
                try:
                    await self.client.send_reaction(peer, msg_id, reaction)
                    logger.debug("Поставлена реакция %s на %s в \"%s\" (%s)", reaction, msg_id, channel_title, date_formatted)
                    return "applied"
                except Exception as e:
                    logger.debug("send_reaction не сработал, пробуем SendReactionRequest: %s", e)

            # fallback — raw API
            try:
                await self.client(SendReactionRequest(
                    peer=peer,
                    msg_id=msg_id,
                    reaction=[ReactionEmoji(emoticon=reaction)]
                ))
                logger.debug("Поставлена реакция %s (fallback) на %s в \"%s\" (%s)", reaction, msg_id, channel_title, date_formatted)
                return "applied"
            except Exception as e:
                logger.exception("Ошибка при установке реакции на %s в \"%s\": %s", msg_id, channel_title, e)
                return "error"

        except Exception as e:
            logger.exception("Неожиданная ошибка в add_reaction: %s", e)
            return "error"

    async def process_history(self, channel, reaction):
        """Обработка истории сообщений с подсчётом успехов/ошибок и компактным логом."""
        try:
            logger.info("Начинаем обработку истории для канала: %s", channel)
            # ввод количества — неблокирующий
            try:
                count_str = await asyncio.to_thread(input, "Сколько предыдущих сообщений обработать?: ")
                count = int(count_str)
            except ValueError:
                logger.error("Некорректное число. Пропускаем.")
                return

            # сколько промежуточных сводок (0 — не показывать)
            log_every = int(os.getenv("PROCESS_LOG_EVERY", "0"))

            logger.info("Будет обработано %d сообщений в %s", count, channel)

            i = 0
            applied = skipped = errors = 0
            start_ts = time.time()

            async for message in self.client.iter_messages(channel, limit=count):
                i += 1
                channel_title = getattr(message.chat, "title", None) or str(channel)
                date_obj = getattr(message, "date", None)
                try:
                    date_formatted = date_obj.strftime("%d-%m-%Y %H:%M") if date_obj else "unknown"
                except Exception:
                    date_formatted = str(date_obj)

                # показываем прогресс для каждой обработки (без отдельного "Готово")
                logger.info("[%d/%d] Обрабатываю сообщение %s в канале \"%s\" время %s", i, count, message.id, channel_title, date_formatted)

                status = await self.add_reaction(message, reaction)
                if status == "applied":
                    applied += 1
                elif status == "skipped":
                    skipped += 1
                else:
                    errors += 1

                # опциональная промежуточная сводка
                if log_every > 0 and (i % log_every == 0 or i == count):
                    logger.info("[%d/%d] Промежуточно: applied=%d skipped=%d errors=%d", i, count, applied, skipped, errors)

                await asyncio.sleep(random.randint(5, 10))

            elapsed = time.time() - start_ts
            elapsed_str = f"{int(elapsed // 60)}m{int(elapsed % 60)}s" if elapsed >= 60 else f"{int(elapsed)}s"
            logger.info("Обработка истории для канала %s завершена: processed=%d/%d applied=%d skipped=%d errors=%d time=%s",
                        channel, i, count, applied, skipped, errors, elapsed_str)

        except Exception as e:
            logger.exception("Ошибка при обработке истории для канала %s: %s", channel, e)

    async def start(self):
        logger.info("start() function called")  # Добавлено логирование
        await self.client.start()
        logger.info("Бот авторизован и запущен")

        # Проверка истории при старте
        logger.info(f"Config.CHANNELS: {Config.CHANNELS}")  # Добавлено логирование
        for ch in Config.CHANNELS:
            logger.info(f"Обрабатываем канал: {ch}")
            await self.process_history(ch.strip(), Config.REACTION)

        logger.info("Завершена обработка истории, начинаю отслеживание новых сообщений")

        # Обработка новых сообщений
        @self.client.on(events.NewMessage(chats=Config.CHANNELS))
        async def handler(event):
            await asyncio.sleep(random.randint(5, 10))  # задержка перед реакцией
            await self.add_reaction(event.message, Config.REACTION)

        await self.client.run_until_disconnected()
