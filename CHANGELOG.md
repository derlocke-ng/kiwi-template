# Changelog

The app's version and the kit's version (`KIT_VERSION`) are released
together under one tag.

## 0.1.2 — 2026-11-19

- **Kit 0.1.2: no toast for every icon change.** Choosing colours and
  styles one after the other to compare them stacked up toasts. The hint
  that the app grid may show the icon only after logging in again is now a
  line under "Appearance"; a toast appears only when the icon could not be
  changed.
- UI rules: buttons that act on the ticked rows of a list sit in the list's
  header, not in the main menu.

## 0.1.1 — 2026-11-19

- **Kit 0.1.1: the stock icon keeps its colour in Flat and Night.** With
  "the app's own" icon chosen, Flat and Night were drawn in the glyph's hue
  (blue for the template) while Classic showed the stock file (green).
  `AppInfo.stock_colorway` names the stock icon's colourway.

## 0.1.0 — 2026-11-19

- **The kit, 0.1.0**: `AppInfo`, the settings file, the remembered window
  size, the worker, the header bar with menu (Help, About), About,
  Preferences with Appearance (app icon chooser from kiwi-icons) and Window,
  and the job strip with the filling kiwi and the output pane.
- **The example app**: notes, with a command and a window.
- **Tools**: `new-app.sh` renames a copy into your app; `kit-update.sh` and
  `kit-check.sh` keep an app's copy of the kit unmodified; `check-version.sh`.
- **UI rules**, accepted on 2026-11-19.
