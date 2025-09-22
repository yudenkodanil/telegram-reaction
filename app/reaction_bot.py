import asyncio
import random
from telethon import TelegramClient, events
from app.logger import logger
from app.config import Config

class ReactionBot:
    def __init__(self):
        self.client = TelegramClient(
            Config.SESSION_FILE,
            Config.API_ID,
            Config.API_HASH
        )

    async def add_reaction(self, message, reaction):
        """Ставит реакцию, если её ещё нет"""
        try:
            # Проверяем, нет ли уже реакции от нас
            reactions = message.reactions
            if reactions and reactions.results:
                for r in reactions.results:
                    if r.reaction.emoticon == reaction and r.chosen_order is not None:
                        logger.info(f"Уже есть реакция {reaction} на сообщение {message.id}")
                        return

            await message.react(reaction)
            logger.info(f"Поставил реакцию {reaction} на сообщение {message.id}")
        except Exception as e:
            logger.error(f"Ошибка при установке реакции: {e}")

    async def process_history(self, channel, reaction):
        """Обработка истории сообщений"""
        need_history = input(f"Обработать предыдущие сообщения в {channel}? (y/n): ").lower()
        if need_history == "y":
            try:
                count = int(input("Сколько предыдущих сообщений обработать?: "))
            except ValueError:
                logger.error("Некорректное число. Пропускаем.")
                return

            async for message in self.client.iter_messages(channel, limit=count):
                await self.add_reaction(message, reaction)
                await asyncio.sleep(random.randint(5, 10))

    async def start(self):
        await self.client.start()
        logger.info("Бот авторизован и запущен")

        # Проверка истории при старте
        for ch in Config.CHANNELS:
            await self.process_history(ch, Config.REACTION)

        # Отслеживание новых постов
        @self.client.on(events.NewMessage(chats=Config.CHANNELS))
        async def handler(event):
            await asyncio.sleep(random.randint(5, 10))  # задержка
            await self.add_reaction(event.message, Config.REACTION)

        await self.client.run_until_disconnected()
