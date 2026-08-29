"""A small, top-most reminder popup used for stretch (and other) prompts."""
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from blush import theme


class ReminderPopup(QDialog):
    def __init__(self, title: str, body: str, parent: QWidget | None = None, timeout: int = 25000):
        super().__init__(parent)
        self.setWindowTitle("blush")
        self.setMinimumWidth(320)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(theme.PALETTE_QSS)

        lay = QVBoxLayout(self)
        head = QLabel(title)
        head.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {theme.C.ACCENT};")
        lay.addWidget(head)

        body_lbl = QLabel(body)
        body_lbl.setWordWrap(True)
        body_lbl.setStyleSheet(f"font-size: 14px; color: {theme.C.TEXT};")
        lay.addWidget(body_lbl)

        row = QHBoxLayout()
        row.addStretch(1)
        ok = QPushButton("ok")
        ok.setObjectName("primary")
        ok.clicked.connect(self.accept)
        row.addWidget(ok)
        lay.addLayout(row)

        if timeout:
            QTimer.singleShot(timeout, self.accept)
