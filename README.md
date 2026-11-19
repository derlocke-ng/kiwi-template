# kiwi-template

kiwi-template is the starting point for a Kiwi Network desktop app: a
command, a GTK 4 window and an installer that
[kiwi-updater](https://github.com/derlocke-ng/kiwi-updater) understands. It is
for anyone who wants to write such an app, and for the existing Kiwi apps,
which move to its layout one by one.

It holds two things. The **kit** (`src/kiwi_template/kit`) is the code every
Kiwi app shares: the header bar and menu, About, Preferences with the icon
chooser, the remembered window size, the settings file, and the job strip
with the filling kiwi. The **example app** around it, a list of notes, shows
the kit in use and is what you replace with your own app. Both follow the
[UI rules](docs/ui-rules.md), so that Kiwi apps look and behave alike.

- Latest release: **v0.1.2**
- In the [development catalog](https://github.com/derlocke-ng/kiwi-catalog-dev),
  not in the Kiwi catalog
- Runs on: Linux with Python 3.11, GTK 4 and libadwaita 1.5; CI tests on
  Ubuntu 24.04
- License: GPL-3.0-or-later

## Use it for your app

On GitHub, press **Use this template**, clone your copy, then:

```bash
tools/new-app.sh kiwi-notes "Kiwi Notes" eu.kiwinetwork.KiwiNotes your-github-name
```

This renames the package, the desktop entry, the icon and every mention.
The kit is not touched. [Starting an app](docs/new-app.md) says what to
replace next.

## Try the example

```bash
./install.sh install
```

```bash
kiwi-template add "buy milk"
```

```bash
kiwi-template-gui
```

The installer copies the app to `~/.local`; it needs no root. In the window,
the menu's "Run the Demo Job" shows the job strip, and the gear opens
Preferences.

## Documentation

| Page | What it covers |
|---|---|
| [Starting an app](docs/new-app.md) | from the template to your own app, step by step |
| [Layout](docs/layout.md) | every folder and file, and what belongs where |
| [The kit](docs/kit.md) | each shared module and how an app uses it |
| [UI rules](docs/ui-rules.md) | what every Kiwi desktop app does the same way |
| [Development](docs/development.md) | tests, CI, versions, releasing the template and the kit |

Release notes: [CHANGELOG.md](CHANGELOG.md).

## Status

Version 0.1.0 has the core of the kit. Not in it yet: snapshots, tags, the
app grid, diagrams, a GNOME extension and a root part. No existing Kiwi app
uses the kit yet.

## License

GPL-3.0-or-later; see [LICENSE](LICENSE).
