# softie

a kawaii self-care desktop companion.
water reminders, stretch breaks, affirmations, and a pastel tray app.

## features

- **water tracker** — log your daily water intake with streak tracking
- **stretch reminders** — gentle nudges to take a break
- **affirmations** — built-in + custom positive affirmations
- **focus mode** — pomodoro-style focus/break sessions
- **breathing pacer** — calming animated breathing exercise
- **daily checklist** — self-care tasks with progress ring
- **pastel themes** — dark and light kawaii palettes
- **system tray** — runs quietly in the background

## install

### nixos

add to your flake inputs:

```nix
inputs = {
  nixpkgs.url = "github:pawprnt/nixpkgs";
};
```

then install:

```nix
environment.systemPackages = [ inputs.nixpkgs.packages.${system}.softie ];
```

or run directly:

```bash
nix run github:pawprnt/nixpkgs#softie
```

### from the aur (arch linux)

```
paru -S softie
```

### from flatpak

```
flatpak remote-add --user pawprnt https://pawprnt.github.io/flatpak-repo/repo
flatpak install --user pawprnt io.github.pawprnt.softie
flatpak run io.github.pawprnt.softie
```

### manual

```
git clone https://github.com/pawprnt/softie.git
cd softie
python -m venv .venv
.venv/bin/pip install -e .
.venv/bin/softie
```

## configuration

settings are stored in `~/.config/softie/settings.json`.

## license

MIT
