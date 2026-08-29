"""Entry point: wire the app, reminder engine, tray, and windows together."""
from __future__ import annotations

import sys

from blush.app import BlushApp
from blush.core import stretches, tracker
from blush.engine import ReminderEngine
from blush.ui.main_window import MainWindow
from blush.ui.reminder_popup import ReminderPopup
from blush.ui.settings_window import SettingsWindow
from blush.ui.tray import TrayIcon


def main() -> int:
    app = BlushApp(sys.argv)
    engine = ReminderEngine()

    def open_main():
        main_win.show()
        main_win.raise_()
        main_win.activateWindow()

    def open_settings():
        settings_win.show()
        settings_win.raise_()
        settings_win.activateWindow()

    def on_drink():
        tracker.record_drink()
        main_win.refresh_water()
        engine.poke("water")

    def show_stretch():
        r = stretches.random_routine()
        ReminderPopup("stretch time~", stretches.format_routine(r)).exec()

    def notify(message: str):
        tray.showMessage("blush", message, tray.icon(), 4000)

    main_win = MainWindow(engine, drink_callback=on_drink)
    settings_win = SettingsWindow(engine)
    tray = TrayIcon(engine, open_main, open_settings)
    engine.stretch_due.connect(show_stretch)
    engine.water_due.connect(lambda: notify("time for a sip of water uwu"))
    engine.affirmation_due.connect(notify)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
