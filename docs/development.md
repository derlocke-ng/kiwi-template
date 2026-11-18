# Development

## Run and test

```bash
make setup     # once: a venv with pytest and ruff; GTK comes from the system
```

```bash
make gui       # the window, from the checkout
```

```bash
make check     # what CI runs, without the linter
```

```bash
make lint
```

The unit tests need no display. CI (`.github/workflows/ci.yml`, Ubuntu
24.04) also runs ruff and shellcheck, imports the window's modules with
GTK 4 and libadwaita, and runs `tools/new-app.sh` on a copy to check that
the renamed app still passes its tests.

The window itself is tested by hand. Without a desktop, GTK's Broadway
backend shows it in a browser:

```bash
gtk4-broadwayd :5 &
GDK_BACKEND=broadway BROADWAY_DISPLAY=:5 make gui    # then open http://localhost:8085
```

## Versions

The version is written in `kiwi.manifest`, `pyproject.toml` and
`src/<package>/__init__.py`; `tools/check-version.sh` fails when they
differ. In kiwi-template the kit's `KIT_VERSION` (`kit/__init__.py`) is
raised together with it whenever a file in `kit/` changed.

After changing the kit, record its files:

```bash
tools/kit-check.sh --write
```

## Releasing

A release is a signed version tag; kiwi installs the newest one.

1. Date the entry in `CHANGELOG.md`.
2. `make check`, commit, push, wait for CI.
3. Tag and push with kiwi-updater's `kiwi-release tag --push`. It signs the
   tag with the release key and refuses a dirty tree or a version that does
   not match.

`.github/workflows/release.yml` then checks the tag's signature against
`.github/allowed_signers` and publishes the release. It is the same file in
every Kiwi app. Signing is described in kiwi-updater's
[Signed releases](https://github.com/derlocke-ng/kiwi-updater/blob/main/docs/signing.md).

## Changing the UI rules

[UI rules](ui-rules.md) is the reference the kit is built to. Change the
rule first, then the kit, then release; apps follow with
`tools/kit-update.sh`.
