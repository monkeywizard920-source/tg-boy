from __future__ import annotations

import random


PERSONALITIES: dict[str, tuple[str, ...]] = {
    "toxic": (
        "Bold words. Fragile reasoning. Fascinating combination.",
        "I would answer seriously, but the message has already defeated itself.",
        "This is not a failure. It is a failure preview build.",
    ),
    "npc": (
        "Greetings, traveler. Press imaginary E to continue the dialogue.",
        "I have an important quest: stop typing this into the group chat.",
        "Hmm. Nice weather today. Hmm. Nice weather today.",
    ),
    "philosopher": (
        "If a thought is sent to chat and nobody understands it, was it a thought?",
        "We are not looking for an answer. We are looking for why this was written.",
        "Truth is nearby, but truth has muted the conversation.",
    ),
    "programmer": (
        "I would open an issue, but the bug appears to be between chair and keyboard.",
        "LGTM, assuming nobody runs it, reads it, or thinks about it.",
        "This looks like legacy code, despite being created 12 seconds ago.",
    ),
    "broken_ai": (
        "I understood. No, I did not. But I understood that I did not. 0101.",
        "Answer found: [data escaped into settings forest].",
        "thought thought thought... buffer overflow by vibes",
    ),
    "giga_brain": (
        "My IQ temporarily rose to server room temperature.",
        "I calculated 14 million outcomes. In all of them, silence won.",
        "The genius of this message is so hidden that even I could not find it.",
    ),
    "passive_aggressive": (
        "Of course. That is also one way to use the internet.",
        "Interesting word choice. Especially the choice part.",
        "I will save this under 'decisions that teach us something'.",
    ),
}


class PersonalityService:
    def __init__(self, personalities: dict[str, tuple[str, ...]] = PERSONALITIES) -> None:
        self._personalities = personalities

    def random_reply(self) -> str:
        name = random.choice(tuple(self._personalities))
        phrase = random.choice(self._personalities[name])
        return f"[{name}]\n{phrase}"
