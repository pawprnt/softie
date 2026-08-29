"""A small always-on-top window showing the focus/break countdown + controls."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget,
)

from softie.core.focus import FocusSession


class FocusWindow(QWidget):
    def __init__(self, session: FocusSession, parent: QWidget | None = None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("softie · focus")
        self.setMinimumSize(300, 220)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        lay = QVBoxLayout(self)

        self.phase = QLabel("ready")
        self.phase.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phase.setObjectName("phase")
        lay.addWidget(self.phase)

        self.clock = QLabel(self._fmt(session.focus_sec))
        self.clock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock.setObjectName("clock")
        lay.addWidget(self.clock)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        lay.addWidget(self.bar)

        row = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("primary")
        self.start_btn.clicked.connect(self._toggle)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self._stop)
        row.addWidget(self.start_btn)
        row.addWidget(self.stop_btn)
        lay.addLayout(row)

        session.tick.connect(self._on_tick)
        session.phase_changed.connect(self._on_phase)

    @staticmethod
    def _fmt(sec: int) -> str:
        sec = max(0, sec)
        return f"{sec // 60:02d}:{sec % 60:02d}"

    def _on_tick(self, remaining: int):
        self.clock.setText(self._fmt(remaining))
        total = self.session.focus_sec if self.session.phase() == "focus" else self.session.break_sec
        frac = (total - remaining) / total if total else 0.0
        self.bar.setValue(int(frac * 100))

    def _on_phase(self, phase: str, remaining: int):
        labels = {"focus": "focus time~", "break": "break time~", "idle": "ready"}
        self.phase.setText(labels.get(phase, phase))
        self.clock.setText(self._fmt(remaining))
        self.start_btn.setText("Stop" if phase != "idle" else "Start")
        self.start_btn.setEnabled(phase != "idle")
        self.stop_btn.setEnabled(phase != "idle")

    def _toggle(self):
        if self.session.is_running():
            self.session.stop()
        else:
            self.session.start()

    def _stop(self):
        self.session.stop()
