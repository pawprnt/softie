"""Short stretch routines shown when a stretch reminder fires."""
from __future__ import annotations

import random

ROUTINES: list[dict] = [
    {
        "name": "neck rolls",
        "steps": [
            "slowly roll your head clockwise, 5 times",
            "then counter-clockwise, 5 times",
            "let your shoulders drop away from your ears",
        ],
    },
    {
        "name": "wrist love",
        "steps": [
            "extend one arm, gently pull fingers back",
            "hold 10s, switch hands",
            "circle each wrist slowly, 5 times",
        ],
    },
    {
        "name": "standing reach",
        "steps": [
            "stand up, interlace fingers, palms out",
            "reach up and lengthen for 10s",
            "softly fold forward and breathe",
        ],
    },
    {
        "name": "hip shift",
        "steps": [
            "step one foot back into a low lunge",
            "breathe into the hip for 15s",
            "switch sides",
        ],
    },
]


def random_routine() -> dict:
    return random.choice(ROUTINES)


def format_routine(routine: dict) -> str:
    return routine["name"] + "\n" + "\n".join(f"- {s}" for s in routine["steps"])
