from __future__ import annotations

import asyncio
import logging
import os
import aiohttp

from aiogram import Bot
from aiogram.exceptions import TelegramNetworkError, TelegramConflictError
from aiohttp import web

from app.bot import create_bot, create_dispatcher
from app.config import Settings
from app.logging_config import setup_logging
from app.repositories.message_repository import MessageRepository
from app.services.context_service import ContextService
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

async def handle_health_check(request):
    return web.Response(text="Bot is alive")

async def start_health_check_server():
    app = web.Application()
    app.router.add_get("/", handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info("Health check server started on port %s", port)

async def keep_alive_ping(url: str | None):
    """Background task to keep the bot alive on Render."""
    if not url:
        logger.warning("RENDER_EXTERNAL_URL not set. Self-ping disabled.")
        return

    logger.info("Self-ping started for URL: %s", url)
    async with aiohttp.ClientSession() as session:
        while True:
            await asyncio.sleep(60)
            try:
                async with session.get(url) as response:
                    logger.debug("Self-ping status: %s", response.status)
            except Exception as e:
                logger.error("Self-ping error: %s", e)

async def main() -> None:
    setup_logging()
    settings = Settings()

    repository = MessageRepository(settings.database_path)
    await repository.init()

    context_service = ContextService(
        repository=repository,
        max_context_messages=settings.max_context_messages,
        max_context_chars=settings.max_context_chars,
    )
    llm_service = LLMService(settings=settings)

    dispatcher = create_dispatcher(
        settings=settings,
        context_service=context_service,
        llm_service=llm_service,
    )

    # Start background health check server for Render
    asyncio.create_task(start_health_check_server())
    asyncio.create_task(keep_alive_ping(settings.render_external_url))

    while True:
        logger.info("Starting Telegram polling")
        bot = create_bot(settings)
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dispatcher.start_polling(bot, skip_updates=True)
        except TelegramConflictError:
            logger.error(
                "Conflict detected: another bot instance is running. "
                "This is normal during Render deploy. Waiting 15 seconds..."
            )
            try:
                await bot.session.close()
            finally:
                await asyncio.sleep(15)
        except TelegramNetworkError as error:
            logger.warning(
                "Telegram API unavailable: %s. Retrying in %s seconds.",
                error,
                settings.polling_retry_delay,
            )
            await bot.session.close()
            await asyncio.sleep(settings.polling_retry_delay)
        else:
            break

if __name__ == "__main__":
    asyncio.run(main())