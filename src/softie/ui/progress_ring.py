"""A small circular progress ring used in the dashboard."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from softie import theme
from softie.theme import THEME


class ProgressRing(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._frac = 0.0
        self.setFixedSize(76, 76)

    def set_fraction(self, frac: float) -> None:
        self._frac = max(0.0, min(1.0, frac))
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = min(w, h) // 2 - 7
        cx, cy = w // 2, h // 2

        painter.setPen(
            QPen(
                QColor(THEME.C.SURFACE_2),
                9,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            )
        )
        painter.drawEllipse(cx - r, cy - r, 2 * r, 2 * r)

        if self._frac > 0:
            span = int(self._frac * 360 * 16)
            painter.setPen(
                QPen(
                    QColor(THEME.C.ACCENT),
                    9,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                )
            )
            painter.drawArc(cx - r, cy - r, 2 * r, 2 * r, 90 * 16, -span)

        painter.setPen(QColor(THEME.C.TEXT))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{int(self._frac * 100)}%")
        painter.end()
