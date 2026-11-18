# Layout

Every Kiwi desktop app has these folders and files. `<package>` is the app's
name with underscores (`kiwi_notes`), `<id>` its application id
(`eu.kiwinetwork.KiwiNotes`).

```
kiwi.manifest            what kiwi reads: name, version, scopes, dependencies
install.sh               install, update, uninstall — run by kiwi
pyproject.toml           version, ruff and pytest settings
Makefile                 make gui | run | test | lint | check
CHANGELOG.md
src/<package>/
  __init__.py            version, application id, the AppInfo the kit gets
  __main__.py, cli.py    the command
  core/                  what the app does. No GTK in here.
  ui/                    the window. Only this imports gi.
    app.py               Adw.Application
    window.py            the main window, built from the kit's parts
  kit/                   the shared code, copied unchanged (see The kit)
scripts/                 bash parts the app runs
data/
  <id>.desktop           the desktop entry
  <id>.svg               the stock icon
tools/                   new-app.sh, kit-update.sh, kit-check.sh, check-version.sh
tests/unit/              pytest, no display needed
docs/                    the pages kiwi-network.eu shows
.github/workflows/       ci.yml, release.yml
.github/allowed_signers  the keys release tags may be signed with
```

## What belongs where

- **`core/` knows nothing about the window.** Anything the window can do, the
  command can do, because both call `core/`. Tests of `core/` need no display.
- **`ui/` holds no logic worth testing.** It shows what `core/` returns and
  calls `core/` when a button is pressed. Work that can take longer than a
  moment goes through the kit's worker or job strip.
- **`kit/` is not yours.** It is the same in every app.
- **Settings** are in `~/.config/<app>/settings.json`, **data** in
  `~/.local/share/<app>/`. Both through `INFO.config_dir()` and
  `INFO.data_dir()`, which respect `XDG_CONFIG_HOME` and `XDG_DATA_HOME`.

## Where the installer puts things

`install.sh` writes only below `~/.local` (`KIWI_PREFIX`):

| Path | What |
|---|---|
| `lib/<app>/<package>/` | the Python package |
| `lib/<app>/scripts/`, `lib/<app>/data/` | bash parts, the stock icon |
| `bin/<app>`, `bin/<app>-gui` | launchers that set `PYTHONPATH` and start Python |
| `share/applications/<id>.desktop` | the desktop entry |
| `share/icons/hicolor/scalable/apps/<id>.svg` | the icon; left alone on update when the user chose one |

Uninstalling removes all of these. `--purge` also removes the settings and
the data.

## Not in this version

A GNOME Shell extension (`extension/`) and a root part (`system/`: daemon,
systemd units, polkit rule, the `system` scope in `install.sh`) are planned
as optional folders. They are not in 0.1.0; kiwi-killswitch is the app to
look at until they are.
