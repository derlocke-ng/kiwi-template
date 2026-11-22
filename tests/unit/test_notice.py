"""The notice bar: says, hides with ✕ until the news changes, runs its button."""

import os

import pytest

if not (os.environ.get("WAYLAND_DISPLAY") or os.environ.get("DISPLAY")):
    # Without a display GTK may still say it initialised and then crash in
    # the first widget (CI did); CI runs this under xvfb-run.
    pytest.skip("no display", allow_module_level=True)

gi = pytest.importorskip("gi", exc_type=ImportError)
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk  # noqa: E402

pytestmark = pytest.mark.skipif(not Gtk.init_check(), reason="no display; GTK cannot initialise")


def test_say_dismiss_and_a_new_key():
    from kiwi_template.kit.notice import Notice

    notice = Notice()
    assert not notice.shown
    notice.say("2 newer snapshots", "Import", lambda: None, key=("a", 1))
    assert notice.shown and notice.label.get_text() == "2 newer snapshots"
    assert notice.button.get_visible() and notice.button.get_label() == "Import"
    notice.close.emit("clicked")
    assert not notice.shown
    notice.say("2 newer snapshots", "Import", lambda: None, key=("a", 1))
    assert not notice.shown, "the same news stays dismissed"
    notice.say("3 newer snapshots", "Import", lambda: None, key=("a", 2))
    assert notice.shown, "new news shows again"


def test_the_button_runs_and_clears():
    from kiwi_template.kit.notice import Notice

    ran = []
    notice = Notice()
    notice.say("news", "Import", lambda: ran.append(1))
    notice.button.emit("clicked")
    assert ran == [1] and not notice.shown
    notice.say("just news")
    assert notice.shown and not notice.button.get_visible()
