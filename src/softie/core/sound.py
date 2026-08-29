"""A soft generated chime played on reminders (no bundled audio assets)."""
from __future__ import annotations

import math
import os
import struct
import tempfile
import wave

_WAV: str | None = None
_EFFECT = None


def _chime_path() -> str:
    global _WAV
    if _WAV and os.path.exists(_WAV):
        return _WAV
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    sr = 44100
    notes = (523.25, 659.25, 783.99)  # gentle C5–E5–G5 arpeggio
    dur = 0.18
    frames: list[int] = []
    for note in notes:
        n = int(sr * dur)
        for i in range(n):
            t = i / sr
            env = max(0.0, 1.0 - t / dur)
            sample = int(32767 * 0.5 * env * math.sin(2 * math.pi * note * t))
            frames.append(sample)
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", x) for x in frames))
    _WAV = path
    return _WAV


def play_chime() -> None:
    global _EFFECT
    try:
        from PySide6.QtCore import QUrl
        from PySide6.QtMultimedia import QSoundEffect
    except Exception:
        return
    if _EFFECT is None:
        _EFFECT = QSoundEffect()
        _EFFECT.setSource(QUrl.fromLocalFile(_chime_path()))
        _EFFECT.setVolume(0.18)
    _EFFECT.play()
