from __future__ import annotations

import random


TERMINAL_BLOCKS: tuple[tuple[str, ...], ...] = (
    (
        "> analyzing human...",
        "> downloading cringe...",
        "> result: user detected",
    ),
    (
        "> booting sarcasm module...",
        "> scanning message quality...",
        "> warning: confidence exceeds evidence",
    ),
    (
        "> sudo explain --why",
        "> permission denied: too dramatic",
        "> fallback: nod and pretend",
    ),
    (
        "> loading braincell_01.dll...",
        "> braincell_01.dll not responding",
        "> switching to vibes mode",
    ),
    (
        "> compiling comeback...",
        "> 0 errors, 47 emotional warnings",
        "> deploy complete",
    ),
)

SYSTEM_MESSAGES: tuple[str, ...] = (
    "[SYSTEM]\nUser classified as suspiciously confident.",
    "[WARNING]\nToo much nonsense detected. Cooling fans emotionally unavailable.",
    "[SYSTEM]\nConversation entered cinematic side-quest mode.",
    "[NOTICE]\nA tiny council has reviewed this message and sighed.",
    "[WARNING]\nMain character energy detected above recommended limits.",
    "[SYSTEM]\nPolite roast generator armed. Safety cap enabled.",
    "[DIAGNOSTIC]\nLogic found: partial. Vibes found: excessive.",
    "[NOTICE]\nThis is a simulated system message. No actual systems were impressed.",
)

FAKE_ERRORS: tuple[str, ...] = (
    "RuntimeError: user.confidence is not supported on this hardware",
    "ValueError: expected thought, got keyboard noise",
    "Segmentation fault (core dumped into the group chat)",
    "HTTP 418: cannot process, I am emotionally a teapot",
    "ImportError: could not import common_sense from current_message",
)


class TerminalService:
    def __init__(
        self,
        terminal_blocks: tuple[tuple[str, ...], ...] = TERMINAL_BLOCKS,
        system_messages: tuple[str, ...] = SYSTEM_MESSAGES,
        fake_errors: tuple[str, ...] = FAKE_ERRORS,
    ) -> None:
        self._terminal_blocks = terminal_blocks
        self._system_messages = system_messages
        self._fake_errors = fake_errors

    def fake_terminal(self) -> str:
        return "```text\n" + "\n".join(random.choice(self._terminal_blocks)) + "\n```"

    def fake_system_message(self) -> str:
        return random.choice(self._system_messages)

    def fake_error(self) -> str:
        return random.choice(self._fake_errors)
