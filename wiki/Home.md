# softie wiki

softie is a kawaii self-care desktop companion for Linux. It lives in your
system tray and gently nudges you to drink water, stretch, read an affirmation,
and tick off a daily self-care checklist — all in a soft pastel theme.

## Quick start

```bash
# Install (PySide6 is expected to be present on the machine)
python -m pip install . --break-system-packages

# Run
softie            # or: python -m softie

# Test (offscreen, no display needed)
QT_QPA_PLATFORM=offscreen python -m pytest
```

## Where things live

- Settings: `~/.config/softie/settings.json`
- Water log: `~/.config/softie/water.json`
- Checklist: `~/.config/softie/checklist.json`

## Pages

- [Features](Features.md)
