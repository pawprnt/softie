"""Per-day water-intake log with a simple consecutive-day streak."""
from __future__ import annotations

import datetime
import json
from pathlib import Path

LOG_DIR = Path.home() / ".config" / "blush"
LOG_FILE = LOG_DIR / "water.json"


def _today() -> str:
    return datetime.date.today().isoformat()


def load_log() -> dict:
    if LOG_FILE.is_file():
        try:
            return json.loads(LOG_FILE.read_text())
        except Exception:
            pass
    return {"date": _today(), "count": 0, "streak": 0}


def record_drink() -> dict:
    log = load_log()
    today = _today()
    if log.get("date") != today:
        log["streak"] = log["streak"] + 1 if log.get("count", 0) > 0 else 0
        log["date"] = today
        log["count"] = 0
    log["count"] = log.get("count", 0) + 1
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(json.dumps(log))
    return log
