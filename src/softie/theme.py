"""Pastel / kawaii palettes for softie, with live dark/light switching.

Widgets use object-name CSS rules (e.g. #title, #clock) so the whole app can
be re-themed at runtime by re-applying the stylesheet.
"""
from __future__ import annotations

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor


class Palette:
    def __init__(self, **kw):
        self.BG = kw["bg"]
        self.SURFACE = kw["surface"]
        self.SURFACE_2 = kw["surface_2"]
        self.ACCENT = kw["accent"]
        self.ACCENT_2 = kw["accent_2"]
        self.MINT = kw["mint"]
        self.TEXT = kw["text"]
        self.TEXT_DIM = kw["text_dim"]
        self.ON_BG = kw.get("on_bg", "#2a1f2e")
        self.RADIUS = kw.get("radius", 14)


DARK = Palette(
    bg="#241f2e", surface="#322a3f", surface_2="#3d3450",
    accent="#ff9ecb", accent_2="#c9b6ff", mint="#b6ffd9",
    text="#fdecf6", text_dim="#b9a9c9", on_bg="#2a1f2e",
)

LIGHT = Palette(
    bg="#fdeef6", surface="#ffffff", surface_2="#f3e3ef",
    accent="#ff7eb6", accent_2="#a98bff", mint="#5fd6a0",
    text="#3a2c3a", text_dim="#8a7a8a", on_bg="#ffffff",
)

VARIANTS = {"dark": DARK, "light": LIGHT}


class Theme(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self._name = "dark"
        self._palette = DARK

    @property
    def C(self):
        return self._palette

    def name(self):
        return self._name

    def set_variant(self, name: str):
        if name not in VARIANTS:
            name = "dark"
        self._name = name
        self._palette = VARIANTS[name]
        self.changed.emit()

    def stylesheet(self) -> str:
        p = self._palette
        return f"""
QWidget {{ background-color: {p.BG}; color: {p.TEXT}; }}
QPushButton {{
    background-color: {p.SURFACE_2}; color: {p.TEXT}; border: none;
    border-radius: {p.RADIUS}px; padding: 8px 16px; font-size: 14px;
}}
QPushButton:hover {{ background-color: {p.ACCENT_2}; }}
QPushButton#primary {{ background-color: {p.ACCENT}; color: {p.ON_BG}; font-weight: 600; }}
QPushButton#primary:hover {{ background-color: {p.MINT}; }}
QLabel {{ color: {p.TEXT}; }}
#title {{ color: {p.ACCENT}; font-size: 26px; font-weight: 700; }}
#subtle {{ color: {p.ACCENT_2}; font-size: 13px; }}
#affirm {{ color: {p.TEXT}; font-size: 14px; padding: 8px 4px; }}
#clock {{ color: {p.TEXT}; font-size: 48px; font-weight: 700; }}
#phase {{ color: {p.ACCENT_2}; font-size: 18px; }}
QLineEdit, QSpinBox, QTextEdit {{
    background-color: {p.SURFACE}; color: {p.TEXT};
    border: 1px solid {p.SURFACE_2}; border-radius: {p.RADIUS}px; padding: 6px 10px;
}}
QCheckBox {{ color: {p.TEXT}; spacing: 8px; }}
QProgressBar {{ background-color: {p.SURFACE_2}; border-radius: {p.RADIUS}px; text-align: center; }}
QProgressBar::chunk {{ background-color: {p.ACCENT}; border-radius: {p.RADIUS}px; }}
QDialog {{ background-color: {p.BG}; }}
"""


THEME = Theme()


def stylesheet() -> str:
    return THEME.stylesheet()


def set_variant(name: str) -> None:
    THEME.set_variant(name)


def qcolor(name: str) -> QColor:
    return QColor(getattr(THEME.C, name))
