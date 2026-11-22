# UI rules for Kiwi desktop apps

Every Kiwi Network desktop app follows these rules, so that someone who knows
one app finds their way in the next. The shared modules of this template (the
kit) implement them; an app that uses the kit follows most of them without
extra work.

**Status: accepted on 2026-11-19, not yet followed.** Each rule says what
the apps did when it was written. Where they disagreed, the rule is marked
**Decided** and says which apps have to change. The kit implements the rules
step by step; an app follows them once it has moved to the kit.

Apps compared: kiwi-fox 0.16.0, kiwi-proxy 0.25.0, kiwi-custodia 0.7.0,
kiwi-server 2.52.0, kiwi-updater 2.8.1 (Kiwi Apps), syncman 0.5.1,
kiwi-killswitch 0.2.3, gnome-monitor 0.3.2.

## 1. Toolkit and colours

- GTK 4 with libadwaita 1.5 or newer. Dialogs are `Adw.Dialog`,
  `Adw.AlertDialog` and `Adw.PreferencesDialog`, not separate windows.
- **The app follows the desktop's light or dark mode. There is no setting for
  it.** Accent colour: the desktop's.
- Custom colours only for status (see rule 9) and for drawings.

Today: all eight apps follow the desktop; none overrides the mode. syncman
still opens two `Adw.Window`s where the others use `Adw.Dialog`, and
kiwi-server has one `Adw.AboutWindow` left.

## 2. The header bar

From left to right:

| Place | What goes there |
|---|---|
| Start (left) | The one main action of the window: **New …** / **Add …**. Nothing else. |
| Middle | The app's name; a short status as subtitle ("14 apps", "3 running"). |
| End (right), from the edge inwards | Main menu (☰), Preferences (gear), Refresh, then the app's own buttons. |

- Every header button has a tooltip.
- An app with a sidebar (kiwi-server) puts the menu in the sidebar's header;
  the rest of the rule applies to the content header.

**Decided** — when written:

| App | Refresh | Gear | Menu ☰ |
|---|---|---|---|
| kiwi-fox, kiwi-proxy, kiwi-custodia | right | right | right |
| kiwi-updater | left | right | none |
| gnome-monitor | left | none (a small gear per row) | right |
| syncman | right | none | none |
| kiwi-server | left, in the content header | none | left, in the sidebar |
| kiwi-killswitch | none | none | none |

The proposal is what kiwi-fox, kiwi-proxy and kiwi-custodia do. kiwi-updater
would move Refresh to the right and gain a menu; syncman and gnome-monitor
would gain a gear and a menu.

## 3. The main menu (☰)

Always, in this order:

1. the app's own window-wide actions ("Stop everything", "Open in Kiwi
   Proxy"), if it has any;
2. **Help** — opens the app's documentation page;
3. **About <App Name>**.

Switches do not go in the menu; they are settings and go in Preferences.
Buttons that act on the ticked rows of a list ("Start Selected") do not go
in the menu either: they sit in the list's header, next to what they act on.

**Decided** — when written only kiwi-fox, kiwi-proxy, kiwi-custodia and kiwi-server
have "About". gnome-monitor keeps two switches ("Ask to Keep Changes",
"Restore Layout at Login") in its menu; they would move to Preferences.
"Help" as a menu item is new for all.

## 4. About

`Adw.AboutDialog`, filled from `kiwi.manifest`, so it cannot disagree with
what `kiwi info` says: name, version, the app's icon, one-line description,
homepage, issue tracker, license, and "Part of Kiwi Network". No credits
list unless the app has one.

Today: four apps have one, each filled by hand.

## 5. Preferences

One `Adw.PreferencesDialog` behind the gear. Its pages, in this order; an
app leaves out what it does not have:

| Page | Groups, in order |
|---|---|
| **General** | the app's own groups first; then **Appearance**; then **Window** |
| **Snapshots** | only for apps that keep data worth backing up (rule 8) |
| **This computer** | maintenance: repair, what is installed where, the uninstall hint |

Fixed groups, the same in every app:

- **Appearance** — "App Icon" and "Icon Style" (rule 6).
- **Window** — "Size" with a Reset button (rule 7); apps that run jobs add
  "Show output while working" (rule 10).

Wording: a row's title is a noun phrase in title case ("App Icon", "Sync
Interval"); the subtitle is a sentence fragment in lower case without a full
stop ("in the app grid, the dash and this window"). A setting takes effect at
once; there is no Save button in Preferences.

**Decided** — when written:

| App | Preferences |
|---|---|
| kiwi-fox, kiwi-custodia | gear; pages General (… , Window) and Snapshots; "This computer" as its own dialog |
| kiwi-proxy | gear; "New exits" and "DNS services"; Snapshots and "This computer" separate |
| kiwi-updater | gear; General: Updates, Packages, Appearance, Window |
| syncman | no dialog; settings sit in the main window between the jobs |
| gnome-monitor | no dialog; two switches in the menu |
| kiwi-server | no dialog |
| kiwi-killswitch | the whole window is settings; it stays as it is |

## 6. Icons

- **The app's own icon** comes from
  [kiwi-icons](https://github.com/derlocke-ng/kiwi-icons) and is drawn by
  `kiwi_icon.py`. Every app offers the same chooser in Preferences →
  Appearance: the stock icon, a colourway, the three styles (Classic, Flat,
  Night), or a file of the user's own from `~/.config/<app>/icons/`. An
  update of the app keeps the choice.
- **Icons of things inside an app** (a browser profile, a box, a sync job)
  are the app's own business, built on the same kit: kiwi-fox may show the
  installed browser's icon, kiwi-custodia gives each box its own colourway.
  The picker for them is the kit's, so it looks the same.
- Buttons use symbolic icons from the icon theme, never bundled bitmaps.

**Decided** — when written only syncman and kiwi-updater have the app-icon chooser.
kiwi-fox and kiwi-custodia colour profiles and boxes but not the app icon.
kiwi-proxy, kiwi-server, kiwi-killswitch and gnome-monitor have no icon
choice. The proposal gives all eight the chooser. The alternative is to drop
it from syncman and kiwi-updater and keep icons fixed.

## 7. Windows

- The main window remembers its size and whether it was maximized, in
  `~/.config/<app>/window.json`. Preferences → Window → Size → Reset goes
  back to the default.
- Default size 1040 × 840 for apps with a list or grid; smaller only for an
  app that is a single form (kiwi-killswitch, 620 × 840).
- The window works down to 360 × 420: it is usable on half a screen.
- Dialog widths: 560 for a form, 720 for details, 900 for long text.

**Decided** — when written five apps remember their size (kiwi-fox, kiwi-proxy,
kiwi-custodia, kiwi-updater, syncman); kiwi-server, kiwi-killswitch and
gnome-monitor do not. Default sizes: 1040 × 840 (kiwi-fox, kiwi-proxy,
kiwi-custodia), 980 × 800 (kiwi-updater), 760 × 820 (syncman), 1180 × 820
(kiwi-server).

## 8. Settings files

In `~/.config/<app>/`:

| File | Holds |
|---|---|
| `settings.json` | what Preferences sets |
| `window.json` | the window's size |
| `icons/` | the user's own icon files |

A missing or broken file means the defaults, never an error. Files are
written to a temporary name and renamed.

**Decided** — when written: `settings.json` (kiwi-fox, kiwi-custodia), `prefs.json`
(kiwi-proxy), `gui.conf` as key=value lines (kiwi-updater, syncman). The
proposal is `settings.json`; the kit reads an old `prefs.json` or `gui.conf`
once and writes the new file.

Snapshots (backups of an app's data into a folder the user chooses): one
module, one page in Preferences, the same words. Today kiwi-fox,
kiwi-proxy and kiwi-custodia each have their own code for it. This rule is
written out when that module is.

## 9. Lists, status and empty states

- Things the app manages are shown as cards in a grid or as rows in a list;
  an app with both lets the user switch and remembers it.
- Status is a small pill with fixed colours: green for running or installed,
  blue for an update, amber for needs root or needs attention, red for
  failed, grey for off.
- Tags and categories are chips above the list that filter it, with a count.
- An empty list is an `Adw.StatusPage` that says what the app is for and has
  the main action as a button.
- A problem that blocks the app is an `Adw.Banner` with one button that
  fixes it. News the user may want to act on, now or later, is the kit's
  notice under the header: one line, one button, and ✕ (newer snapshots in
  the folder: "2 newer snapshots in your folder: work, shop · Import · ✕").
  ✕ hides it until the news changes. A result is a toast; a setting that visibly changed (a switch,
  a new icon in the preview) needs none. A question is an `Adw.AlertDialog`; a
  destructive answer is red and never the default.

Today: pills, chips and the grid exist in kiwi-updater; tags in kiwi-fox;
banners, toasts and alert dialogs are already used the same way in most apps;
the notice for newer snapshots in Kiwi Proxy, Kiwi Fox and Kiwi Custodia.

## 10. Work in progress

- Work never blocks the window: it runs in the kit's worker and the window
  stays usable.
- A short check (refresh) shows the thin bar under the header.
- A job the user started (install, start, build) shows the job strip at the
  bottom: the filling kiwi, the job's name, and "2 of 5 done". Where there is
  nothing to count, the kiwi goes round.
- The command's own output is in a terminal pane under the strip, unchanged.
  Preferences → Window → "Show output while working" decides whether it
  opens with a job; it always opens when a job fails.

Today: only kiwi-updater 2.8.1 has the strip, the kiwi and the switch.
kiwi-fox, kiwi-proxy and kiwi-custodia share one worker module already.

## 11. Words

- The app's name in title case in the UI ("Kiwi Fox"); the command in lower
  case with a dash (`kiwi-fox`).
- Buttons say what they do in one or two words: "Install", "Stop", "Take
  down". Not "OK", not "Yes".
- The same thing has the same word in every app: **Refresh**, **Preferences**,
  **About**, **Remove** (takes it off a list), **Delete** (destroys data),
  **Uninstall** (an app).
- Help text behind a (?) button is at most three sentences and links to the
  docs page.
