"""Settings persistence for softie (~/.config/softie/settings.json)."""
from __future__ import annotations

import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "softie"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULTS: dict = {
    "water": {"enabled": True, "interval_min": 60},
    "stretch": {"enabled": True, "interval_min": 45},
    "affirmation": {"enabled": True, "interval_min": 120},
    "affirmations": [],
    "checklist": ["take meds", "go for a walk", "journal a line"],
    "focus": {"focus_min": 25, "break_min": 5},
    "theme": "dark",
    "sound": {"enabled": True},
}


def load() -> dict:
    data: dict = {}
    if CONFIG_FILE.is_file():
        try:
            data = json.loads(CONFIG_FILE.read_text())
        except Exception:
            data = {}
    return _merge(DEFAULTS, data)


def save(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def _merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out
