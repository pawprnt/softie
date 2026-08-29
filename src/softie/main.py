"""Entry point: wire the app, reminder engine, tray, and windows together."""
from __future__ import annotations

import sys

from softie.app import BlushApp
from softie.core import stretches, tracker
from softie.core.config import load as load_config
from softie.core.focus import FocusSession
from softie.core.sound import play_chime
from softie.engine import ReminderEngine
from softie.theme import THEME, set_variant, stylesheet
from softie.ui.focus_window import FocusWindow
from softie.ui.main_window import MainWindow
from softie.ui.breathing_window import BreathingWindow
from softie.ui.reminder_popup import ReminderPopup
from softie.ui.settings_window import SettingsWindow
from softie.ui.tray import TrayIcon, make_icon


def main() -> int:
    app = BlushApp(sys.argv)
    engine = ReminderEngine()

    set_variant(load_config().get("theme", "dark"))
    app.setStyleSheet(stylesheet())

    def open_main():
        main_win.show()
        main_win.raise_()
        main_win.activateWindow()

    def open_settings():
        settings_win.show()
        settings_win.raise_()
        settings_win.activateWindow()

    def open_focus():
        focus_win.show()
        focus_win.raise_()
        focus_win.activateWindow()

    def open_breathe():
        breathe_win.show()
        breathe_win.raise_()
        breathe_win.activateWindow()

    def on_drink():
        tracker.record_drink()
        main_win.refresh_water()
        engine.poke("water")

    def show_stretch():
        chime()
        r = stretches.random_routine()
        ReminderPopup("stretch time~", stretches.format_routine(r)).exec()

    def notify(message: str):
        tray.showMessage("softie", message, tray.icon(), 4000)
        chime()

    def chime():
        if load_config().get("sound", {}).get("enabled", True):
            play_chime()

    def apply_runtime():
        set_variant(load_config().get("theme", "dark"))
        app.setStyleSheet(stylesheet())

    fc = load_config().get("focus", {})
    focus = FocusSession(
        focus_min=fc.get("focus_min", 25),
        break_min=fc.get("break_min", 5),
    )
    focus.phase_changed.connect(
        lambda phase, _rem: notify(
            "focus time~ lock in uwu" if phase == "focus" else "break time~ stretch or sip water"
        )
    )

    main_win = MainWindow(engine, drink_callback=on_drink, on_breathe=open_breathe)
    settings_win = SettingsWindow(engine)
    focus_win = FocusWindow(focus)
    breathe_win = BreathingWindow()
    tray = TrayIcon(engine, open_main, open_settings, open_focus, open_breathe)
    engine.stretch_due.connect(show_stretch)
    engine.water_due.connect(lambda: notify("time for a sip of water uwu"))
    engine.affirmation_due.connect(notify)

    settings_win.accepted.connect(apply_runtime)
    THEME.changed.connect(lambda: tray.setIcon(make_icon()))

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
