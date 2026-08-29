"""Reminder timers that emit signals when it's time to care for yourself."""
from __future__ import annotations

from PySide6.QtCore import QObject, QTimer, Signal

from blush.core import config, affirmations

_NAMES = ("water", "stretch", "affirmation")


class ReminderEngine(QObject):
    water_due = Signal()
    stretch_due = Signal()
    affirmation_due = Signal(str)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._cfg = config.load()
        self._timers: dict[str, QTimer] = {}
        for name in _NAMES:
            self._setup(name)

    def reload(self, cfg: dict | None = None) -> None:
        self._cfg = cfg or config.load()
        for name in _NAMES:
            self._setup(name)

    def _setup(self, name: str) -> None:
        timer = self._timers.get(name)
        if timer is None:
            timer = QTimer(self)
            timer.timeout.connect(lambda n=name: self._fire(n))
            self._timers[name] = timer
        spec = self._cfg.get(name, {})
        if spec.get("enabled") and spec.get("interval_min", 0) > 0:
            timer.start(int(spec["interval_min"]) * 60 * 1000)
        else:
            timer.stop()

    def _fire(self, name: str) -> None:
        if name == "water":
            self.water_due.emit()
        elif name == "stretch":
            self.stretch_due.emit()
        else:
            self.affirmation_due.emit(
                affirmations.random_affirmation(self._cfg.get("affirmations"))
            )

    def poke(self, name: str) -> None:
        """Manual trigger (e.g. 'I drank water') and restart that interval."""
        self._fire(name)
        timer = self._timers.get(name)
        if timer is not None and timer.isActive():
            timer.start()
