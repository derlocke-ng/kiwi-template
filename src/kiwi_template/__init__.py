"""kiwi-template — the starting point for a Kiwi Network desktop app.

A small working app: a list of notes with a command-line tool and a GTK
window. It exists to show the layout and the kit (kiwi_template/kit) in use;
tools/new-app.sh turns a copy of it into your app.
"""

from pathlib import Path

from .kit import AppInfo

__version__ = "0.1.3"
APP = "kiwi-template"
# The GTK application's id. The desktop entry and the icon are named after it,
# which is how GNOME on Wayland connects the window to its entry.
APP_ID = "eu.kiwinetwork.KiwiTemplate"
NAME = "Kiwi Template"
HOMEPAGE = "https://github.com/derlocke-ng/kiwi-template"

# install.sh puts data/ next to the package; in a checkout it is two levels up.
_HERE = Path(__file__).resolve().parent
_DATA = next(
    (d for d in (_HERE.parent / "data", _HERE.parent.parent / "data") if d.is_dir()), _HERE
)

INFO = AppInfo(
    app=APP,
    app_id=APP_ID,
    name=NAME,
    version=__version__,
    description="Starting point for a Kiwi Network desktop app: bash, Python, GTK 4",
    homepage=HOMEPAGE,
    docs=f"{HOMEPAGE}/blob/main/docs/README.md",
    glyph="plugin",
    stock_colorway="kiwi",
    stock_icon=_DATA / f"{APP_ID}.svg",
)
SCRIPTS = next(
    (d for d in (_HERE.parent / "scripts", _HERE.parent.parent / "scripts") if d.is_dir()), _HERE
)
