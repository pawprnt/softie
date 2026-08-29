import pytest

from blush.core import config, affirmations
from blush.engine import ReminderEngine
from blush.ui.tray import make_icon


def test_config_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_FILE", tmp_path / "s.json")
    monkeypatch.setattr(config, "CONFIG_DIR", tmp_path)
    cfg = config.load()
    assert cfg["water"]["interval_min"] == 60
    assert cfg["water"]["enabled"] is True
    cfg["water"]["interval_min"] = 30
    config.save(cfg)
    assert config.load()["water"]["interval_min"] == 30


def test_config_merge(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_FILE", tmp_path / "s.json")
    monkeypatch.setattr(config, "CONFIG_DIR", tmp_path)
    config.save({"water": {"interval_min": 10}})
    cfg = config.load()
    assert cfg["stretch"]["enabled"] is True
    assert cfg["water"]["interval_min"] == 10


def test_affirmations():
    assert isinstance(affirmations.random_affirmation(), str)
    samples = {affirmations.random_affirmation(["only this one"]) for _ in range(100)}
    assert "only this one" in samples


def test_engine_construct(app):
    e = ReminderEngine()
    assert e._cfg["water"]["enabled"] is True
    got = []
    e.water_due.connect(lambda: got.append(1))
    e.poke("water")
    assert got == [1]


def test_engine_reload_disables(app):
    e = ReminderEngine()
    e.reload({
        "water": {"enabled": False, "interval_min": 5},
        "stretch": {"enabled": False, "interval_min": 5},
        "affirmation": {"enabled": False, "interval_min": 5},
    })
    assert e._timers["water"].isActive() is False


def test_icon(app):
    assert not make_icon().isNull()
