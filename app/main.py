import asyncio
from app.reaction_bot import ReactionBot
from app.logger import logger

async def main():
    bot = ReactionBot()
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную")
