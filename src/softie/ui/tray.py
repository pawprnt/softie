"""System tray icon + menu for softie."""
from __future__ import annotations

from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from softie import theme


def make_icon(size: int = 64) -> QIcon:
    px = QPixmap(size, size)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(theme.C.ACCENT))
    p.drawEllipse(6, 6, size - 12, size - 12)
    p.setBrush(QColor(theme.C.ACCENT_2))
    p.drawEllipse(int(size * 0.34), int(size * 0.30), int(size * 0.32), int(size * 0.32))
    p.end()
    return QIcon(px)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, engine, open_main, open_settings, parent: QObject | None = None):
        super().__init__(make_icon(), parent)
        self.setToolTip("softie")
        self.engine = engine

        menu = QMenu()
        menu.addAction("Open", open_main)
        menu.addAction("I drank water", lambda: engine.poke("water"))
        menu.addAction("Stretch now", lambda: engine.poke("stretch"))
        menu.addAction("Affirmation", lambda: engine.poke("affirmation"))
        menu.addSeparator()
        menu.addAction("Settings", open_settings)
        menu.addAction("Quit", QApplication.quit)
        self.setContextMenu(menu)
        self.activated.connect(
            lambda reason: reason == QSystemTrayIcon.ActivationReason.DoubleClick
            and open_main()
        )
        self.show()
