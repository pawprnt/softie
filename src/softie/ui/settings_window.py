"""Settings dialog: reminder intervals, enable toggles, custom affirmations."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox, QDialog, QDialogButtonBox, QFormLayout, QLabel, QSpinBox,
    QTextEdit, QVBoxLayout,
)

from softie import theme
from softie.core import config


class SettingsWindow(QDialog):
    def __init__(self, engine, parent: QWidget | None = None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("softie · settings")
        self.setMinimumWidth(360)
        self.setStyleSheet(theme.PALETTE_QSS)

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
        cfg["affirmations"] = [
            line.strip() for line in self.affirm.toPlainText().splitlines() if line.strip()
        ]
        config.save(cfg)
        self.engine.reload(cfg)
        self.accept()
