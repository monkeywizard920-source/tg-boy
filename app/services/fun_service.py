from __future__ import annotations

import asyncio
import logging
import random
from collections.abc import Awaitable, Callable

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.types import FSInputFile, Message

from app.config import Settings
from app.services.achievement_service import AchievementService
from app.services.image_service import ImageService
from app.services.personality_service import PersonalityService
from app.services.terminal_service import TerminalService

logger = logging.getLogger(__name__)


FUN_ACTION_WEIGHTS: dict[str, int] = {
    "achievement": 50,
    "fake_error": 50,
    "fake_ban": 50,
    "terminal": 50,
    "system": 50,
    "personality": 50,
    "thinking": 50,
    "iq": 50,
    "broken_ai": 50,
    "overdramatic": 50,
    "image": 35,
    "meme_reply": 50,
}

MEME_REPLIES: tuple[str, ...] = (
    "I have seen many messages, but this one is DLC for chaos.",
    "One second, I am checking whether this is a thought or a trailer for one.",
    "Your request has been accepted, judged, and placed on the tiny shelf.",
    "This message passed the vibe check and failed the technical inspection.",
    "Group chat, stay strong. We have a local earthquake of meaning.",
)

THINKING_REPLIES: tuple[str, ...] = (
    "thinking...",
    "thinking...\nstill thinking...\nregretting thinking...",
    "thinking.exe is looking for a reason to continue",
)

BROKEN_REPLIES: tuple[str, ...] = (
    "I I I think think think I understood understood 01001000 01000101 01001100 01010000",
    "Answer: yes. No. Maybe. [consciousness left the chat]",
    "01010111 01001000 01011001\nwhy why why",
    "System stable. Stable. Sta... ble... 0110.",
)

OVERDRAMATIC_REPLIES: tuple[str, ...] = (
    "I read that message and somewhere on the server a tiny light of hope went out.",
    "Human history is now divided into before this message and after. Both eras are concerning.",
    "The sky darkened, fans accelerated, and I am still trying to answer with dignity.",
    "This is not just text. This is an emotional operation against common sense.",
)

IMAGE_TEXTS: tuple[str, ...] = (
    "official certificate: user is suspiciously confident",
    "the meme committee reviewed this request and left for tea",
    "there could have been a smart thought here, but fun mode arrived",
    "white image of judgment",
    "your IQ has been sent for additional review",
)


class FunService:
    def __init__(
        self,
        *,
        settings: Settings,
        achievement_service: AchievementService,
        image_service: ImageService,
        personality_service: PersonalityService,
        terminal_service: TerminalService,
        action_weights: dict[str, int] | None = None,
    ) -> None:
        self._settings = settings
        self._achievement_service = achievement_service
        self._image_service = image_service
        self._personality_service = personality_service
        self._terminal_service = terminal_service
        self._action_weights = action_weights or FUN_ACTION_WEIGHTS

    async def try_handle(self, *, bot: Bot, message: Message, question: str) -> bool:
        if random.random() > self._settings.fun_trigger_chance:
            return False

        action = self._choose_action()
        logger.info("Fun mode selected action=%s chat_id=%s", action, message.chat.id)

        handlers: dict[str, Callable[[Bot, Message, str], Awaitable[None]]] = {
            "achievement": self._send_achievement,
            "fake_error": self._send_fake_error,
            "fake_ban": self._send_fake_ban,
            "terminal": self._send_terminal,
            "system": self._send_system,
            "personality": self._send_personality,
            "thinking": self._send_thinking,
            "iq": self._send_iq,
            "broken_ai": self._send_broken_ai,
            "overdramatic": self._send_overdramatic,
            "image": self._send_image,
            "meme_reply": self._send_meme_reply,
        }

        handler = handlers.get(action)
        if handler is None:
            logger.warning("Unknown fun action: %s", action)
            return False

        try:
            await self._maybe_fake_typing(bot, message)
            await handler(bot, message, question)
            return True
        except Exception as error:
            logger.exception("Fun action failed: %s", error)
            return False

    def _choose_action(self) -> str:
        actions = tuple(self._action_weights.keys())
        weights = tuple(self._action_weights.values())
        return random.choices(actions, weights=weights, k=1)[0]

    async def _maybe_fake_typing(self, bot: Bot, message: Message) -> None:
        if random.random() > 0.65:
            return

        delay = random.uniform(0.4, 2.4)
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        await asyncio.sleep(delay)

    async def _send_achievement(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(self._achievement_service.random_achievement()))

    async def _send_fake_error(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(self._terminal_service.fake_error()))

    async def _send_fake_ban(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(
            "\u0412\u044b \u0437\u0430\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d\u044b"
        )
        await asyncio.sleep(2)
        await message.answer("\u043b\u0430\u0434\u043d\u043e \u0448\u0443\u0447\u0443")

    async def _send_terminal(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(self._terminal_service.fake_terminal()))

    async def _send_system(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(self._terminal_service.fake_system_message()))

    async def _send_personality(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(self._personality_service.random_reply()))

    async def _send_thinking(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(random.choice(THINKING_REPLIES)))

    async def _send_iq(self, bot: Bot, message: Message, question: str) -> None:
        iq = random.randint(3, 404)
        await message.answer(f"Random user IQ: {iq}\nMethodology: absolutely not scientific.")

    async def _send_broken_ai(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(random.choice(BROKEN_REPLIES)))

    async def _send_overdramatic(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(random.choice(OVERDRAMATIC_REPLIES)))

    async def _send_meme_reply(self, bot: Bot, message: Message, question: str) -> None:
        await message.answer(self._trim(random.choice(MEME_REPLIES)))

    async def _send_image(self, bot: Bot, message: Message, question: str) -> None:
        text = random.choice(IMAGE_TEXTS)
        if question.strip():
            text = f"{text}\n\nInput:\n{question[:220]}"

        path = self._image_service.create_text_image(self._trim(text))
        try:
            await message.answer_photo(FSInputFile(path), caption="fun mode artifact")
        finally:
            self._image_service.cleanup(path)

    def _trim(self, text: str) -> str:
        return text[: self._settings.fun_max_reply_chars]
