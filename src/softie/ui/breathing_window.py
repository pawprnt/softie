"""A calming breathing pacer: a soft circle that expands/contracts to guide breath."""
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QWidget,
)

from softie.theme import THEME


class _Circle(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._r = 30
        self.setMinimumSize(200, 200)

    def set_radius(self, r: float):
        self._r = r
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        pal = THEME.C
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(pal.ACCENT_2))
        p.drawEllipse(cx - self._r - 8, cy - self._r - 8, 2 * (self._r + 8), 2 * (self._r + 8))
        p.setBrush(QColor(pal.ACCENT))
        p.drawEllipse(cx - self._r, cy - self._r, 2 * self._r, 2 * self._r)
        p.end()


class BreathingWindow(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("softie · breathe")
        self.setMinimumSize(280, 330)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self._phases = [
            ("breathe in", 4000, "expand"),
            ("hold", 2000, "big"),
            ("breathe out", 4000, "contract"),
            ("hold", 2000, "small"),
        ]
        self._idx = 0
        self._elapsed = 0
        self._min, self._max = 28, 96
        self._radius = self._min

        lay = QVBoxLayout(self)
        self.label = QLabel("breathe in")
        self.label.setObjectName("phase")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.label)

        self.canvas = _Circle()
        THEME.changed.connect(self.canvas.update)
        lay.addWidget(self.canvas)

        close = QPushButton("close")
        close.setObjectName("primary")
        close.clicked.connect(self.close)
        lay.addWidget(close)

        self._timer = QTimer(self)
        self._timer.setInterval(30)
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    def _tick(self):
        _, dur, kind = self._phases[self._idx]
        self._elapsed += self._timer.interval()
        t = min(1.0, self._elapsed / dur)
        if kind == "expand":
            self._radius = self._min + (self._max - self._min) * self._ease(t)
        elif kind == "contract":
            self._radius = self._max - (self._max - self._min) * self._ease(t)
        self.label.setText(self._phases[self._idx][0])
        self.canvas.set_radius(self._radius)
        if self._elapsed >= dur:
            self._elapsed = 0
            self._idx = (self._idx + 1) % len(self._phases)

    @staticmethod
    def _ease(t: float) -> float:
        return t * t * (3 - 2 * t)
