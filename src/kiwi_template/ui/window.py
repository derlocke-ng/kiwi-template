"""The main window: a list of notes, built from the kit's parts.

What is the kit's and what is the app's:
  kit   header bar, menu, About, Preferences (Appearance, Window), window
        size, settings file, job strip, output pane, notice bar
  app   the list, the "New Note" dialog, the app's own Preferences group
"""

from __future__ import annotations

from gi.repository import Adw, Gio, GLib, Gtk

from .. import INFO, SCRIPTS
from ..core import notes
from ..kit import geometry, header, worker
from ..kit.notice import Notice
from ..kit.prefs import Preferences
from ..kit.progress import JobArea
from ..kit.settings import Store

# The app's own settings, with their defaults. The kit adds its "kit.*" keys.
DEFAULTS = {"demo_steps": 4}


class Window(Adw.ApplicationWindow):
    def __init__(self, **kwargs) -> None:
        super().__init__(title=INFO.name, **kwargs)
        self.store = Store(INFO, DEFAULTS)
        geometry.restore(self, INFO)

        demo = Gio.SimpleAction.new("demo-job", None)
        demo.connect("activate", lambda *_a: self.run_demo())
        self.add_action(demo)
        news = Gio.SimpleAction.new("demo-notice", None)
        news.connect("activate", lambda *_a: self.demo_notice())
        self.add_action(news)

        self.jobs = JobArea(self.store)
        self.header = header.build(
            self,
            INFO,
            main=("New Note", "list-add-symbolic", self.new_note),
            on_refresh=self.refresh,
            on_preferences=self.open_preferences,
            menu_actions=[
                ("Run the Demo Job", "win.demo-job"),
                ("Show the Demo Notice", "win.demo-notice"),
            ],
            extra_end=[self.jobs.output_button],
        )

        self.list = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, valign=Gtk.Align.START)
        self.list.add_css_class("boxed-list")
        clamp = Adw.Clamp(
            child=self.list,
            maximum_size=720,
            margin_top=18,
            margin_bottom=18,
            margin_start=12,
            margin_end=12,
        )
        self.empty = Adw.StatusPage(
            icon_name=INFO.app_id,
            title="No Notes Yet",
            description="This is the template's example app. Add a note, or run the "
            "demo job from the menu to see the job strip.",
        )
        add = Gtk.Button(label="New Note", halign=Gtk.Align.CENTER)
        add.add_css_class("pill")
        add.add_css_class("suggested-action")
        add.connect("clicked", lambda *_a: self.new_note())
        self.empty.set_child(add)
        self.stack = Gtk.Stack(vexpand=True)
        self.stack.add_named(Gtk.ScrolledWindow(child=clamp), "list")
        self.stack.add_named(self.empty, "empty")

        self.toasts = Adw.ToastOverlay()
        body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        body.append(self.stack)
        body.append(self.jobs)
        self.toasts.set_child(body)
        view = Adw.ToolbarView(content=self.toasts)
        view.add_top_bar(self.header)
        self.notice = Notice()  # under the header: news to act on, with ✕
        view.add_top_bar(self.notice)
        self.set_content(view)
        self.refresh()

    # ── the list ──────────────────────────────────────────────────────────
    def refresh(self) -> None:
        """Reading can block (a slow disk, a network folder): off the main loop."""
        worker.run(notes.load, self.show, lambda exc: self.toast(str(exc)))

    def show(self, items: list[str]) -> None:
        self.list.remove_all()
        for index, text in enumerate(items):
            row = Adw.ActionRow(title=GLib.markup_escape_text(text))
            remove = Gtk.Button(
                icon_name="user-trash-symbolic", valign=Gtk.Align.CENTER, tooltip_text="Remove"
            )
            remove.add_css_class("flat")
            remove.connect("clicked", lambda _b, i=index: self.remove_note(i))
            row.add_suffix(remove)
            self.list.append(row)
        self.stack.set_visible_child_name("list" if items else "empty")
        count = len(items)
        self.header.kit_title.set_subtitle(f"{count} note{'' if count == 1 else 's'}")

    def new_note(self) -> None:
        dialog = Adw.AlertDialog(heading="New Note")
        entry = Gtk.Entry(placeholder_text="What to remember", activates_default=True)
        dialog.set_extra_child(entry)
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("add", "Add")
        dialog.set_response_appearance("add", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("add")
        dialog.set_close_response("cancel")

        def on_response(_dialog, response: str) -> None:
            if response != "add":
                return
            try:
                self.show(notes.add(entry.get_text()))
            except (ValueError, OSError) as exc:
                self.toast(str(exc))

        dialog.connect("response", on_response)
        dialog.present(self)

    def remove_note(self, index: int) -> None:
        try:
            self.show(notes.remove(index))
        except (IndexError, OSError) as exc:
            self.toast(str(exc))

    # ── a job ─────────────────────────────────────────────────────────────
    def run_demo(self) -> None:
        if self.jobs.busy:
            self.toast("A job is already running")
            return
        steps = self.store["demo_steps"]
        self.jobs.run(
            f"Demo job in {steps} steps",
            ["bash", str(SCRIPTS / "demo-job.sh"), str(steps)],
            steps=steps,
            is_step=lambda line: line.startswith("step "),
            on_done=lambda rc: self.toast("Demo job finished" if rc == 0 else "Demo job failed"),
        )

    # ── a notice ──────────────────────────────────────────────────────────
    def demo_notice(self) -> None:
        """What an app says when, say, its snapshot folder has newer copies."""
        self.notice.say(
            "A newer copy of your notes is in the snapshot folder",
            "Import",
            lambda: self.toast("Imported (a demo: nothing changed)"),
        )

    # ── preferences ───────────────────────────────────────────────────────
    def open_preferences(self) -> None:
        group = Adw.PreferencesGroup(title="Demo Job")
        steps = Adw.SpinRow.new_with_range(1, 12, 1)
        steps.set_title("Steps")
        steps.set_subtitle("how many parts the demo job has")
        steps.set_value(self.store["demo_steps"])
        steps.connect(
            "notify::value", lambda row, _p: self.store.set("demo_steps", int(row.get_value()))
        )
        group.add(steps)
        Preferences(INFO, self.store, self, own_groups=[group], jobs=True).present(self)

    def toast(self, text: str) -> None:
        self.toasts.add_toast(Adw.Toast(title=GLib.markup_escape_text(text)))
