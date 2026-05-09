from __future__ import annotations

import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from app.config import Settings
from app.handlers.chat import router as chat_router
from app.handlers.admin import router as admin_router
from app.services.achievement_service import AchievementService
from app.services.context_service import ContextService
from app.services.fun_service import FunService
from app.services.image_service import ImageService
from app.services.llm_service import LLMService
from app.services.chat_control_service import ChatControlService
from app.services.personality_service import PersonalityService
from app.services.terminal_service import TerminalService

logger = logging.getLogger(__name__)

def create_bot(settings: Settings) -> Bot:
    session_kwargs = {}
    if settings.telegram_api_base_url:
        session_kwargs["api"] = TelegramAPIServer.from_base(settings.telegram_api_base_url)

    session = AiohttpSession(
        timeout=settings.telegram_request_timeout,
        **session_kwargs,
    )
    bot = Bot(token=settings.bot_token, session=session)
    logger.info(f"Bot created with token: {settings.bot_token[:5]}...")
    return bot

def create_dispatcher(
    *,
    settings: Settings,
    context_service: ContextService,
    llm_service: LLMService,
) -> Dispatcher:
    achievement_service = AchievementService()
    image_service = ImageService()
    personality_service = PersonalityService()
    terminal_service = TerminalService()
    fun_service = FunService(
        settings=settings,
        achievement_service=achievement_service,
        image_service=image_service,
        personality_service=personality_service,
        terminal_service=terminal_service,
    )

    dispatcher = Dispatcher(
        settings=settings,
        context_service=context_service,
        llm_service=llm_service,
        chat_control=ChatControlService(context_service._repository),
        fun_service=fun_service,
    )
    dispatcher.include_router(admin_router)
    dispatcher.include_router(chat_router)
    return dispatcher
