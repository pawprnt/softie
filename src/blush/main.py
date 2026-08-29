"""Entry point: wire the app, reminder engine, tray, and windows together."""
from __future__ import annotations

import sys

from blush.app import BlushApp
from blush.engine import ReminderEngine
from blush.ui.main_window import MainWindow
from blush.ui.settings_window import SettingsWindow
from blush.ui.tray import TrayIcon


def main() -> int:
    app = BlushApp(sys.argv)
    engine = ReminderEngine()
    main_win = MainWindow(engine)
    settings_win = SettingsWindow(engine)

    def open_main():
        main_win.show()
        main_win.raise_()
        main_win.activateWindow()

    def open_settings():
        settings_win.show()
        settings_win.raise_()
        settings_win.activateWindow()

    tray = TrayIcon(engine, open_main, open_settings)

    def notify(message: str):
        tray.showMessage("blush", message, tray.icon(), 4000)

    engine.water_due.connect(lambda: notify("time for a sip of water uwu"))
    engine.stretch_due.connect(lambda: notify("stretch your body for a moment~"))
    engine.affirmation_due.connect(notify)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
