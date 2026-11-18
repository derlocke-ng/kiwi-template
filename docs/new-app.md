# Starting an app

This page takes you from the template to an app of your own that `kiwi` can
install.

## 1. Copy and rename

On GitHub, press **Use this template** on
[kiwi-template](https://github.com/derlocke-ng/kiwi-template) and clone your
new repository. Then run, once:

```bash
tools/new-app.sh kiwi-notes "Kiwi Notes" eu.kiwinetwork.KiwiNotes your-github-name
```

| Argument | Meaning |
|---|---|
| `kiwi-notes` | the command and repository name: lower case letters, digits, dashes |
| `"Kiwi Notes"` | the name as the window and the app grid write it |
| `eu.kiwinetwork.KiwiNotes` | the application id: the reverse of a domain you own, then the name |
| `your-github-name` | where the repository lives; default `derlocke-ng` |

The script renames `src/kiwi_template` to `src/kiwi_notes`, the two files in
`data/`, and every mention in the other files. It leaves the kit and `docs/`
alone. Check that it worked:

```bash
make check
```

## 2. Replace the example

| File | What to do |
|---|---|
| `src/<package>/core/notes.py` | replace with what your app manages. Keep it free of GTK: the command and the window both use it. |
| `src/<package>/cli.py` | your commands |
| `src/<package>/ui/window.py` | your window. Keep the calls into the kit; replace the list and the dialog. |
| `scripts/demo-job.sh` | your bash parts, or delete it |
| `data/<id>.svg` | your icon. For a Kiwi Network app, take it from [kiwi-icons](https://github.com/derlocke-ng/kiwi-icons) and set `glyph=` in `__init__.py`. |
| `kiwi.manifest`, `data/<id>.desktop` | description, category, tags, dependencies |
| `README.md`, `docs/` | write your own; delete the pages about the template |

Do not edit `src/<package>/kit`. [The kit](kit.md) says why and how to
update it.

## 3. Try it

```bash
make gui
```

runs the window from the checkout.

```bash
./install.sh install
```

installs it to `~/.local`, as `kiwi` would.

## 4. Let kiwi install it

Push the repository, then on a machine with kiwi-updater:

```bash
kiwi add https://github.com/your-github-name/kiwi-notes.git
```

```bash
kiwi install kiwi-notes
```

kiwi installs the newest version tag, or the default branch while there is
none. Manifest keys, dependencies and signed releases are described in
kiwi-updater's
[Writing an app](https://github.com/derlocke-ng/kiwi-updater/blob/main/docs/app-authors.md).
