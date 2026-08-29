"""QApplication subclass that applies the pastel theme."""
from __future__ import annotations

from PySide6.QtWidgets import QApplication

from softie import theme


class BlushApp(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.setApplicationName("softie")
        self.setStyleSheet(theme.stylesheet())
