import pytest

from softie.core import config, affirmations, tracker, stretches, checklist, focus
from softie.engine import ReminderEngine
from softie.theme import THEME, stylesheet
from softie.ui.tray import make_icon


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


def test_water_log(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "LOG_FILE", tmp_path / "water.json")
    monkeypatch.setattr(tracker, "LOG_DIR", tmp_path)
    log = tracker.record_drink()
    assert log["count"] == 1
    assert log["streak"] == 0
    log = tracker.record_drink()
    assert log["count"] == 2
    reloaded = tracker.load_log()
    assert reloaded["count"] == 2


def test_stretches():
    assert isinstance(stretches.random_routine(), dict)
    body = stretches.format_routine(stretches.ROUTINES[0])
    assert "neck rolls" in body and "- " in body


def test_config_defaults(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(config, "CONFIG_FILE", tmp_path / "s.json")
    cfg = config.load()
    assert cfg["theme"] == "dark"
    assert cfg["sound"]["enabled"] is True
    assert cfg["focus"]["focus_min"] == 25
    assert cfg["checklist"]


def test_breathing(app):
    from softie.ui.breathing_window import BreathingWindow

    w = BreathingWindow()
    w._idx = 0  # breathe in (expand)
    w._elapsed = 2000
    r0 = w._radius
    w._tick()
    assert w._radius > r0, "should expand on breathe in"

    w._idx = 2  # breathe out (contract)
    w._elapsed = 2000
    r1 = w._radius
    w._tick()
    assert w._radius < r1, "should contract on breathe out"
    w.close()


def test_theme_variant():
    THEME.set_variant("light")
    assert THEME.name() == "light"
    assert THEME.C.BG != "#241f2e"
    ss = stylesheet()
    assert THEME.C.BG in ss
    THEME.set_variant("dark")
    assert THEME.name() == "dark"


def test_checklist(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_FILE", tmp_path / "s.json")
    monkeypatch.setattr(config, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(checklist, "DATA_FILE", tmp_path / "c.json")
    monkeypatch.setattr(checklist, "DATA_DIR", tmp_path)

    checklist.set_tasks(["a", "b"])
    assert checklist.tasks() == ["a", "b"]
    assert checklist.progress() == 0.0

    checklist.toggle("a")
    assert checklist.is_done("a") is True
    assert abs(checklist.progress() - 0.5) < 1e-9

    checklist.toggle("a")
    assert checklist.is_done("a") is False
    assert checklist.progress() == 0.0

    checklist.set_tasks([])
    assert checklist.progress() == 0.0


def test_focus_session(app):
    s = focus.FocusSession(focus_min=25, break_min=5)
    phases = []
    s.phase_changed.connect(lambda p, d: phases.append((p, d)))
    assert s.is_running() is False
    s.start()
    assert s.is_running() is True
    assert phases and phases[0][0] == "focus"
    # force a focus -> break transition
    s.focus_sec = 1
    s._remaining = 1
    s._on_tick()
    assert phases[-1][0] == "break"
    s.stop()
    assert s.is_running() is False
    assert phases[-1][0] == "idle"
