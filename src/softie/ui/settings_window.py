"""Settings dialog: reminder intervals, enable toggles, custom affirmations."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLabel,
    QSpinBox, QTextEdit, QVBoxLayout, QWidget,
)

from softie.core import config
from softie.theme import THEME


class SettingsWindow(QDialog):
    def __init__(self, engine, parent: QWidget | None = None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("softie · settings")
        self.setMinimumWidth(360)

        cfg = engine._cfg
        lay = QVBoxLayout(self)
        form = QFormLayout()
        self._rows = {}
        for name, label in (
            ("water", "Water"),
            ("stretch", "Stretch"),
            ("affirmation", "Affirmation"),
        ):
            spec = cfg.get(name, {})
            on = QCheckBox()
            on.setChecked(bool(spec.get("enabled", True)))
            mins = QSpinBox()
            mins.setRange(1, 600)
            mins.setValue(int(spec.get("interval_min", 60)))
            form.addRow(label, on)
            form.addRow("  every (min)", mins)
            self._rows[name] = (on, mins)
        lay.addLayout(form)

        focus = cfg.get("focus", {})
        flay = QFormLayout()
        self.focus_min = QSpinBox()
        self.focus_min.setRange(1, 180)
        self.focus_min.setValue(int(focus.get("focus_min", 25)))
        self.break_min = QSpinBox()
        self.break_min.setRange(1, 60)
        self.break_min.setValue(int(focus.get("break_min", 5)))
        flay.addRow("Focus (min)", self.focus_min)
        flay.addRow("Break (min)", self.break_min)
        box = QWidget()
        box.setLayout(flay)
        box.setStyleSheet(f"QLabel {{ color: {THEME.C.TEXT_DIM}; }}")
        lay.addWidget(QLabel("Focus mode"))
        lay.addWidget(box)

        self.theme_box = QComboBox()
        self.theme_box.addItems(["dark", "light"])
        self.theme_box.setCurrentText(str(cfg.get("theme", "dark")))
        self.sound_on = QCheckBox()
        self.sound_on.setChecked(bool(cfg.get("sound", {}).get("enabled", True)))
        alay = QFormLayout()
        alay.addRow("Theme", self.theme_box)
        alay.addRow("Chime on reminders", self.sound_on)
        abox = QWidget()
        abox.setLayout(alay)
        abox.setStyleSheet(f"QLabel {{ color: {THEME.C.TEXT_DIM}; }}")
        lay.addWidget(QLabel("Appearance & audio"))
        lay.addWidget(abox)

        lay.addWidget(QLabel("Custom affirmations (one per line, optional)"))
        self.affirm = QTextEdit()
        self.affirm.setPlainText("\n".join(cfg.get("affirmations") or []))
        lay.addWidget(self.affirm)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def _save(self):
        cfg = self.engine._cfg
        for name, (on, mins) in self._rows.items():
            cfg[name] = {"enabled": on.isChecked(), "interval_min": mins.value()}
        cfg["focus"] = {
            "focus_min": self.focus_min.value(),
            "break_min": self.break_min.value(),
        }
        cfg["theme"] = self.theme_box.currentText()
        cfg["sound"] = {"enabled": self.sound_on.isChecked()}
        cfg["affirmations"] = [
            line.strip() for line in self.affirm.toPlainText().splitlines() if line.strip()
        ]
        config.save(cfg)
        self.engine.reload(cfg)
        self.accept()
