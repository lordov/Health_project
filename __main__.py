import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage

from fluentogram import TranslatorHub

from redis.asyncio.client import Redis
from redis.exceptions import ConnectionError

from aiogram_dialog import setup_dialogs

from tgbot.dialogs.Standart_dialog import start_dialog
from tgbot.dialogs.admin_dialog import admin_panel
from tgbot.dialogs.survay_dialog import survay_dialog
from tgbot.handlers import router_list

from tgbot.database.engine import create_db, session_maker

from tgbot.utils.logger_config import configure_logging
from tgbot.utils.commands import set_commands
from tgbot.utils.i18n import create_translator_hub
from tgbot.middlewares.i18n import TranslatorRunnerMiddleware
from tgbot.middlewares.db import DataBaseSession
from tgbot.config import BOT_TOKEN


async def setup_dispatcher() -> Dispatcher:
    """
    Function to set up the dispatcher (Dispatcher).

    Tries to establish a connection with Redis and creates a data storage
    (RedisStorage) or, if the connection with Redis fails, uses a data storage
    in memory (MemoryStorage).

    Returns:
        Dispatcher: The aiogram dispatcher object.
    """

    # Create a Redis client
    redis = Redis()

    try:
        # Try to ping Redis
        await redis.ping()

        # If successful, create a Redis storage
        storage = RedisStorage(
            redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    except ConnectionError:
        # If Redis is not available, use a memory storage instead
        print("Redis is not available, using MemoryStorage instead.")
        storage = MemoryStorage()

    # Create a dispatcher with the chosen storage
    dp = Dispatcher(storage=storage)

    return dp


async def setup_bot(dp: Dispatcher):
    """
    Function to set up the bot (Bot).
    Here we also register routers and dialogs.

    Args:
        dp (Dispatcher): The aiogram dispatcher object.

    Returns:
        Bot: The aiogram bot object.
    """

    # Create a bot object with the provided token and default properties
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))

    # Include all the routers
    dp.include_routers(*router_list)

    # Include the admin panel, start dialog, and survey dialog routers
    dp.include_routers(admin_panel, start_dialog, survay_dialog)

    # Register internationalization
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.update.middleware(TranslatorRunnerMiddleware())

    # Set up the dialogs
    setup_dialogs(dp)

    # Return the bot object
    return bot


async def main():
    """
    Main function to run the bot.

    This function sets up the dispatcher, bot, and starts the bot polling.
    """

    # Set up the dispatcher with the chosen storage
    dp: Dispatcher = await setup_dispatcher()

    # Set up the bot with the provided token and default properties
    bot: Bot = await setup_bot(dp)

    # Create the database
    await create_db()

    # Set the bot commands
    await set_commands(bot)

    # Create the translator hub
    translator_hub: TranslatorHub = create_translator_hub()

    # Delete the webhook and send a message to the admin
    await bot.delete_webhook(drop_pending_updates=True)

    # Start the bot polling with the translator hub
    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == '__main__':
    configure_logging()
    asyncio.run(main())
