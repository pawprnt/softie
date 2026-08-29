"""QApplication subclass that applies the pastel theme."""
from __future__ import annotations

from PySide6.QtWidgets import QApplication

from blush import theme


class BlushApp(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.setApplicationName("blush")
        self.setStyleSheet(theme.PALETTE_QSS)
