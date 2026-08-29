"""A small, soft dashboard: daily checklist, water streak, quick actions."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QWidget,
)

from softie.core import affirmations, checklist, tracker
from softie.theme import THEME
from softie.ui.progress_ring import ProgressRing


class MainWindow(QWidget):
    def __init__(self, engine=None, drink_callback=None, on_breathe=None, parent: QWidget | None = None):
        super().__init__(parent)
        self.engine = engine
        self._drink_callback = drink_callback
        self._on_breathe = on_breathe
        self.setWindowTitle("softie")
        self.setMinimumSize(360, 520)

        lay = QVBoxLayout(self)

        top = QHBoxLayout()
        title = QLabel("softie")
        title.setObjectName("title")
        top.addWidget(title)
        top.addStretch(1)
        self.ring = ProgressRing()
        THEME.changed.connect(self.ring.update)
        top.addWidget(self.ring)
        lay.addLayout(top)

        self.water_label = QLabel()
        self.water_label.setObjectName("subtle")
        lay.addWidget(self.water_label)

        self.list_widget = QWidget()
        self.list_lay = QVBoxLayout(self.list_widget)
        self.list_lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.list_widget)

        add_row = QHBoxLayout()
        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("add a self-care task…")
        self.add_input.returnPressed.connect(self._add_task)
        add_btn = QPushButton("add")
        add_btn.setObjectName("primary")
        add_btn.clicked.connect(self._add_task)
        add_row.addWidget(self.add_input)
        add_row.addWidget(add_btn)
        lay.addLayout(add_row)

        self.affirm = QLabel(affirmations.random_affirmation())
        self.affirm.setWordWrap(True)
        self.affirm.setObjectName("affirm")
        lay.addWidget(self.affirm)

        row = QHBoxLayout()
        b_water = QPushButton("I drank water")
        b_water.setObjectName("primary")
        b_water.clicked.connect(self._water)
        b_stretch = QPushButton("Stretch")
        b_stretch.clicked.connect(self._stretch)
        b_breathe = QPushButton("Breathe")
        b_breathe.clicked.connect(self._breathe)
        row.addWidget(b_water)
        row.addWidget(b_stretch)
        row.addWidget(b_breathe)
        lay.addLayout(row)

        self._rebuild_list()
        self.refresh()

    def _rebuild_list(self):
        while self.list_lay.count():
            item = self.list_lay.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        done = checklist.done_set()
        for task in checklist.tasks():
            row = QHBoxLayout()
            cb = QCheckBox(task)
            cb.setChecked(task in done)
            cb.toggled.connect(
                lambda checked, t=task: self._toggle(t, checked)
            )
            rm = QPushButton("×")
            rm.setFixedWidth(26)
            rm.setToolTip("remove task")
            rm.clicked.connect(lambda _=False, t=task: self._remove(t))
            row.addWidget(cb)
            row.addStretch(1)
            row.addWidget(rm)
            wrap = QWidget()
            wrap.setLayout(row)
            self.list_lay.addWidget(wrap)
        self.list_lay.addStretch(1)

    def _toggle(self, task: str, checked: bool):
        if checked:
            checklist.toggle(task)
        else:
            checklist.toggle(task)
        self.refresh()

    def _add_task(self):
        name = self.add_input.text().strip()
        if name:
            checklist.set_tasks(checklist.tasks() + [name])
            self.add_input.clear()
            self._rebuild_list()
            self.refresh()

    def _remove(self, task: str):
        checklist.set_tasks([t for t in checklist.tasks() if t != task])
        self._rebuild_list()
        self.refresh()

    def refresh(self):
        log = tracker.load_log()
        self.water_label.setText(
            f"water: {log['count']} today  ·  {log['streak']} day streak"
        )
        self.ring.set_fraction(checklist.progress())

    def showEvent(self, event):
        self._rebuild_list()
        self.refresh()
        super().showEvent(event)

    def _water(self):
        if self._drink_callback:
            self._drink_callback()
        else:
            if self.engine:
                self.engine.poke("water")
        self.refresh()
        self.affirm.setText(affirmations.random_affirmation())

    def _stretch(self):
        if self.engine:
            self.engine.poke("stretch")
        self.affirm.setText(affirmations.random_affirmation())

    def _breathe(self):
        if self._on_breathe:
            self._on_breathe()
