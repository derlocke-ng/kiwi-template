#!/usr/bin/env bash
# install.sh — kiwi-template, installed by `kiwi` (see kiwi.manifest)
#
# User scope only: nothing outside $HOME is written.
#
#   KIWI_SCOPE  user        KIWI_PREFIX  ~/.local
#   KIWI_ACTION install|update|uninstall
#   KIWI_GUI    0 on a headless machine
#   KIWI_PURGE  1 only when the user asked for --purge
set -euo pipefail

KIWI_SCOPE="${KIWI_SCOPE:-user}"
KIWI_PREFIX="${KIWI_PREFIX:-$HOME/.local}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP=kiwi-template
PKG=kiwi_template
DESKTOP_ID=eu.kiwinetwork.KiwiTemplate   # the GTK application id: entry and icon carry it
LIBDIR="$KIWI_PREFIX/lib/$APP"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}/$APP"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/$APP"
ICON="$KIWI_PREFIX/share/icons/hicolor/scalable/apps/$DESKTOP_ID.svg"

if [[ "$KIWI_SCOPE" != user ]]; then
    echo "install.sh: $APP is user-scope only; nothing to do for scope '$KIWI_SCOPE'"
    exit 0
fi

refresh_desktop_caches() {
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -qtf "$KIWI_PREFIX/share/icons/hicolor" 2>/dev/null || true
    fi
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database -q "$KIWI_PREFIX/share/applications" 2>/dev/null || true
    fi
}

# Has the user chosen an icon in Preferences → Appearance? Then an update
# must not put the stock one back (the kit wrote theirs to $ICON).
custom_icon() {
    [[ -f "$CONFIG/settings.json" ]] || return 1
    python3 - "$CONFIG/settings.json" <<'PY'
import json, sys
try:
    s = json.load(open(sys.argv[1]))
except (OSError, ValueError):
    sys.exit(1)
custom = s.get("kit.icon_file") or s.get("kit.icon_color") or s.get("kit.icon_style", "classic") != "classic"
sys.exit(0 if custom else 1)
PY
}

launcher() { # name  python-module
    cat > "$KIWI_PREFIX/bin/$1" <<EOW
#!/usr/bin/env bash
export PYTHONPATH="$LIBDIR\${PYTHONPATH:+:\$PYTHONPATH}"
exec python3 -m $2 "\$@"
EOW
    chmod +x "$KIWI_PREFIX/bin/$1"
}

do_install() {
    mkdir -p "$LIBDIR" "$KIWI_PREFIX/bin"
    rm -rf "${LIBDIR:?}/$PKG" "$LIBDIR/scripts" "$LIBDIR/data"
    cp -r "$SRC/src/$PKG" "$LIBDIR/$PKG"
    cp -r "$SRC/scripts" "$LIBDIR/scripts"
    # the stock icon, kept for "back to the stock icon" in Preferences
    install -Dm644 "$SRC/data/$DESKTOP_ID.svg" "$LIBDIR/data/$DESKTOP_ID.svg"
    find "$LIBDIR" -name __pycache__ -type d -prune -exec rm -rf {} +

    launcher "$APP" "$PKG"

    if [[ "${KIWI_GUI:-1}" == 1 ]]; then
        launcher "$APP-gui" "$PKG.ui"
        # Entry and icon are named after the GTK application id, so GNOME links
        # the window to them; Exec is the launcher's absolute path, as the app
        # grid may not have ~/.local/bin on its PATH.
        mkdir -p "$KIWI_PREFIX/share/applications"
        sed "s|^Exec=.*|Exec=$KIWI_PREFIX/bin/$APP-gui|" "$SRC/data/$DESKTOP_ID.desktop" \
            > "$KIWI_PREFIX/share/applications/$DESKTOP_ID.desktop"
        if ! custom_icon; then
            install -Dm644 "$SRC/data/$DESKTOP_ID.svg" "$ICON"
        fi
        refresh_desktop_caches
    fi

    echo "installed $APP to $KIWI_PREFIX"
    echo "  $APP list        the command"
    echo "  $APP-gui         the window (\"Kiwi Template\" in your app grid)"
}

do_uninstall() {
    rm -f "$KIWI_PREFIX/bin/$APP" "$KIWI_PREFIX/bin/$APP-gui"
    rm -f "$KIWI_PREFIX/share/applications/$DESKTOP_ID.desktop" "$ICON"
    rm -rf "${LIBDIR:?}"
    refresh_desktop_caches
    if [[ "${KIWI_PURGE:-0}" == 1 || "${2:-}" == --purge ]]; then
        echo "purging $DATA and $CONFIG"
        rm -rf "${DATA:?}" "${CONFIG:?}"
    else
        echo "kept $DATA and $CONFIG (pass --purge to remove them)"
    fi
    echo "uninstalled $APP"
}

case "${KIWI_ACTION:-${1:-install}}" in
    install|update) do_install ;;
    uninstall)      do_uninstall "$@" ;;
    *) echo "usage: $0 install|update|uninstall [--purge]" >&2; exit 1 ;;
esac
