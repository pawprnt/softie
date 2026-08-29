"""A small, soft dashboard window for the latest affirmation + quick actions."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from blush import theme
from blush.core import affirmations


class MainWindow(QWidget):
    def __init__(self, engine=None, parent: QWidget | None = None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("blush")
        self.setMinimumSize(360, 320)
        self.setStyleSheet(theme.PALETTE_QSS)

        lay = QVBoxLayout(self)
        title = QLabel("blush")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {theme.C.ACCENT};")
        lay.addWidget(title)

        self.affirm = QLabel(affirmations.random_affirmation())
        self.affirm.setWordWrap(True)
        self.affirm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.affirm.setStyleSheet(f"font-size: 16px; color: {theme.C.TEXT}; padding: 12px;")
        lay.addWidget(self.affirm)

        row = QHBoxLayout()
        b_water = QPushButton("I drank water")
        b_water.setObjectName("primary")
        b_water.clicked.connect(self._water)
        b_stretch = QPushButton("Stretch")
        b_stretch.clicked.connect(self._stretch)
        row.addWidget(b_water)
        row.addWidget(b_stretch)
        lay.addLayout(row)
        lay.addStretch(1)

    def _water(self):
        if self.engine:
            self.engine.poke("water")
        self.affirm.setText(affirmations.random_affirmation())

    def _stretch(self):
        if self.engine:
            self.engine.poke("stretch")
        self.affirm.setText(affirmations.random_affirmation())
