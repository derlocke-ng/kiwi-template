# The kit

The kit is the folder `src/<package>/kit`. It is the same in every Kiwi app:
copied from kiwi-template, never edited in an app. An app tells it who it is
with one `AppInfo` and gets the parts of the window that all Kiwi apps share,
built as the [UI rules](ui-rules.md) say.

This page describes kit 0.1.2.

## Why a copy

kiwi installs an app by cloning its repository; there is no package manager
that could bring a shared library along. So each app carries the kit, at a
version it was tested with, and one app's update cannot break another.

What keeps the copies the same is `tools/kit-check.sh`. It compares the
kit's files with the list in `kit/KIT.sha256` and fails if one differs; CI
runs it. To change the kit, change it in kiwi-template, release it, and
update the apps:

```bash
tools/kit-update.sh            # the newest kiwi-template release
```

```bash
tools/kit-update.sh v0.2.0     # that release
```

```bash
tools/kit-update.sh ../kiwi-template   # a local checkout, to try a change
```

## Telling the kit who the app is

In `src/<package>/__init__.py`:

```python
from .kit import AppInfo

INFO = AppInfo(
    app="kiwi-notes",                    # command and folder name
    app_id="eu.kiwinetwork.KiwiNotes",   # GTK application id
    name="Kiwi Notes",                   # as the UI writes it
    version=__version__,
    description="One line, as in kiwi.manifest",
    homepage="https://github.com/you/kiwi-notes",
    glyph="files",                       # a kiwi-icons glyph, for the icon chooser
    stock_icon=_DATA / "eu.kiwinetwork.KiwiNotes.svg",
)
```

Optional: `stock_colorway` (the kiwi-icons colourway of your stock icon,
when it is not the glyph's own colour; Flat and Night of the stock choice
are drawn in it), `docs` (the page Help opens; default: the homepage),
`default_size` (default 1040 × 840), `min_size` (default 360 × 420).

## The modules

| Module | What it gives the app | UI rule |
|---|---|---|
| `info` | `AppInfo`, with `config_dir()`, `data_dir()`, `cache_dir()` | |
| `settings` | `Store`: `~/.config/<app>/settings.json` | 8 |
| `geometry` | the window remembers its size | 7 |
| `worker` | `run(work, on_done, on_error)`: work off the main loop | 10 |
| `header` | the header bar and the main menu with Help and About | 2, 3 |
| `about` | the About dialog | 4 |
| `prefs` | `Preferences`: General with Appearance and Window | 5 |
| `icon` | the app icon the user chose, written for the desktop | 6 |
| `progress` | `JobArea`: job strip, filling kiwi, output pane | 10 |
| `kiwi_icon` | [kiwi-icons](https://github.com/derlocke-ng/kiwi-icons)' kit, unchanged | 6 |

### Settings

```python
store = Store(INFO, {"repair_on_start": True})   # your keys and their defaults
store["repair_on_start"]                          # read
store.set("repair_on_start", False)               # write, at once
```

A missing or broken file gives the defaults. A stored value of the wrong
type gives the default. Keys the app did not declare stay in the file. The
kit's own keys start with `kit.`.

### Window, header, menu

```python
geometry.restore(self, INFO)          # in the window's __init__
self.header = header.build(
    self, INFO,
    main=("New Note", "list-add-symbolic", self.new_note),
    on_refresh=self.refresh,
    on_preferences=self.open_preferences,
    menu_actions=[("Stop Everything", "win.stop-all")],
    extra_end=[self.jobs.output_button],
)
```

`header.kit_title` is the title widget (set its subtitle for a short
status), `header.kit_refresh` the Refresh button. The kit adds the actions
`win.about`, `win.help` (F1), `win.preferences` (Ctrl+,) and `win.refresh`
(Ctrl+R).

### Preferences

```python
Preferences(INFO, self.store, self, own_groups=[my_group], jobs=True).present(self)
```

`own_groups` are the app's `Adw.PreferencesGroup`s; they come first on the
General page, before Appearance and Window. `jobs=True` adds "Show Output
While Working". Further pages: `dialog.add(page)`.

The installer must leave the installed icon alone when the user chose one;
the template's `install.sh` does (`custom_icon`).

### Jobs

```python
self.jobs = JobArea(self.store)       # append it at the bottom of the window
self.jobs.run("Build the image", ["podman", "build", "."],
              steps=4, is_step=lambda line: line.startswith("STEP "),
              on_done=lambda returncode: ...)
```

The strip shows the label and "2 of 4 done" while the kiwi fills; with
`steps=0` the kiwi goes round. The command's output goes to the pane below,
which opens with the job unless the user switched that off, and always opens
when the job fails. For work that is not one command, call `start`, `log`,
`step` and `finish` yourself. One job runs at a time; `jobs.busy` says
whether one does.

## Not in the kit yet

Snapshots, tags and filter chips, status pills, the app grid, diagrams and a
help button. The UI rules already describe some of them; they are added as
they are taken out of the apps that have them.
