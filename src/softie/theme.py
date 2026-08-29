"""Pastel / kawaii palette for softie (femboy-adjacent soft plum + pink/lavender)."""
from __future__ import annotations

from PySide6.QtGui import QColor


class C:
    BG = "#241f2e"
    SURFACE = "#322a3f"
    SURFACE_2 = "#3d3450"
    ACCENT = "#ff9ecb"
    ACCENT_2 = "#c9b6ff"
    MINT = "#b6ffd9"
    TEXT = "#fdecf6"
    TEXT_DIM = "#b9a9c9"
    RADIUS = 14


PALETTE_QSS = f"""
QWidget {{ background-color: {C.BG}; color: {C.TEXT}; }}
QPushButton {{
    background-color: {C.SURFACE_2}; color: {C.TEXT}; border: none;
    border-radius: {C.RADIUS}px; padding: 8px 16px; font-size: 14px;
}}
QPushButton:hover {{ background-color: {C.ACCENT_2}; }}
QPushButton#primary {{ background-color: {C.ACCENT}; color: #2a1f2e; font-weight: 600; }}
QPushButton#primary:hover {{ background-color: {C.MINT}; }}
QLabel {{ color: {C.TEXT}; }}
QLineEdit, QSpinBox, QTextEdit {{
    background-color: {C.SURFACE}; color: {C.TEXT};
    border: 1px solid {C.SURFACE_2}; border-radius: {C.RADIUS}px; padding: 6px 10px;
}}
QCheckBox {{ color: {C.TEXT}; spacing: 8px; }}
QDialog {{ background-color: {C.BG}; }}
"""


def qcolor(name: str) -> QColor:
    return QColor(getattr(C, name))
