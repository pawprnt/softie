"""Pomodoro-style focus sessions: alternating focus/break cycles."""
from __future__ import annotations

from PySide6.QtCore import QObject, QTimer, Signal


class FocusSession(QObject):
    tick = Signal(int)
    phase_changed = Signal(str, int)

    def __init__(self, focus_min: int = 25, break_min: int = 5, parent: QObject | None = None):
        super().__init__(parent)
        self.focus_sec = max(1, int(focus_min)) * 60
        self.break_sec = max(1, int(break_min)) * 60
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)
        self._remaining = 0
        self._phase = "idle"
        self._running = False

    def start(self):
        if self._running:
            return
        self._phase = "focus"
        self._remaining = self.focus_sec
        self._running = True
        self._timer.start()
        self.phase_changed.emit(self._phase, self._remaining)
        self.tick.emit(self._remaining)

    def stop(self):
        if not self._running:
            return
        self._timer.stop()
        self._running = False
        self._phase = "idle"
        self.phase_changed.emit(self._phase, 0)

    def is_running(self):
        return self._running

    def phase(self):
        return self._phase

    def _on_tick(self):
        self._remaining -= 1
        if self._remaining <= 0:
            if self._phase == "focus":
                self._phase = "break"
                self._remaining = self.break_sec
            else:
                self._phase = "focus"
                self._remaining = self.focus_sec
            self.phase_changed.emit(self._phase, self._remaining)
        self.tick.emit(self._remaining)
