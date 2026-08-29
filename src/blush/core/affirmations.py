"""Wholesome affirmations for the self-care reminders."""
from __future__ import annotations

import random

BUILTIN: list[str] = [
    "you are doing your best and that is enough",
    "tiny steps still move you forward",
    "you deserve softness and rest",
    "your worth is not your productivity",
    "be gentle with yourself today",
    "you are allowed to take up space",
    "breathing slowly is enough for right now",
    "you are cared for, even in the small moments",
    "rest is part of the work, not a detour from it",
    "you are softer and stronger than you know",
]


def random_affirmation(custom: list[str] | None = None) -> str:
    pool = list(BUILTIN)
    if custom:
        pool += [a for a in custom if a and a.strip()]
    return random.choice(pool) if pool else "be kind to yourself"
