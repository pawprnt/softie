"""Daily self-care checklist with per-day completion reset."""
from __future__ import annotations

import datetime
import json
from pathlib import Path

from softie.core import config

DATA_DIR = config.CONFIG_DIR
DATA_FILE = DATA_DIR / "checklist.json"


def _today() -> str:
    return datetime.date.today().isoformat()


def tasks() -> list[str]:
    return list(config.load().get("checklist") or [])


def set_tasks(names: list[str]) -> None:
    cfg = config.load()
    cfg["checklist"] = [n.strip() for n in names if n.strip()]
    config.save(cfg)


def _load_day() -> dict:
    if DATA_FILE.is_file():
        try:
            data = json.loads(DATA_FILE.read_text())
        except Exception:
            data = {}
    else:
        data = {}
    if data.get("date") != _today():
        data = {"date": _today(), "done": []}
        _save(data)
    return data


def done_set() -> set[str]:
    return set(_load_day().get("done", []))


def is_done(task: str) -> bool:
    return task in done_set()


def toggle(task: str) -> bool:
    day = _load_day()
    done = set(day.get("done", []))
    if task in done:
        done.discard(task)
    else:
        done.add(task)
    day["done"] = list(done)
    _save(day)
    return task in done


def progress() -> float:
    ts = tasks()
    if not ts:
        return 0.0
    done = done_set()
    return len(done & set(ts)) / len(ts)


def _save(day: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(day))
