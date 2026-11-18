"""The kit's parts that need no display."""

import json

import pytest

from kiwi_template.kit import AppInfo, geometry, icon
from kiwi_template.kit.settings import Store


@pytest.fixture
def info(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    stock = tmp_path / "stock.svg"
    stock.write_text("<svg>stock</svg>")
    return AppInfo(
        app="t-app",
        app_id="org.example.T",
        name="T App",
        version="1",
        glyph="plugin",
        stock_icon=stock,
    )


def test_settings_defaults_and_roundtrip(info):
    store = Store(info, {"steps": 4})
    assert store["steps"] == 4 and store["kit.show_output"] is True
    store.set("steps", 7)
    assert Store(info, {"steps": 4})["steps"] == 7
    with pytest.raises(KeyError):
        store.set("unknown", 1)


def test_settings_broken_file_and_wrong_type(info):
    path = info.config_dir() / "settings.json"
    path.parent.mkdir(parents=True)
    path.write_text("{ not json")
    assert Store(info, {"steps": 4})["steps"] == 4
    path.write_text(json.dumps({"steps": "many", "other": 1}))
    store = Store(info, {"steps": 4})
    assert store["steps"] == 4
    store.set("steps", 5)
    assert json.loads(path.read_text())["other"] == 1  # unknown keys are kept


def test_geometry_default_and_minimum(info):
    assert geometry.saved(info) == (1040, 840, False)
    (info.config_dir()).mkdir(parents=True)
    (info.config_dir() / "window.json").write_text(
        '{"width": 10, "height": 900, "maximized": true}'
    )
    assert geometry.saved(info) == (360, 900, True)


def test_icon_stock_colour_own_and_back(info):
    store = Store(info)
    assert not icon.is_custom(store)
    assert icon.apply(info, store) is None
    assert icon.target(info).read_text() == "<svg>stock</svg>"

    store.set("kit.icon_color", "ocean")
    store.set("kit.icon_style", "night")
    assert icon.is_custom(store) and icon.apply(info, store) is None
    assert (
        icon.target(info).read_text().startswith("<svg")
        and "stock" not in icon.target(info).read_text()
    )

    info.icons_dir().mkdir(parents=True)
    (info.icons_dir() / "mine.png").write_bytes(b"\x89PNG fake")
    (info.icons_dir() / "notes.txt").write_text("no")
    assert icon.own_files(info) == ["mine.png"]
    store.set("kit.icon_file", "mine.png")
    assert icon.apply(info, store) is None
    assert "data:image/png;base64," in icon.target(info).read_text()

    for key, value in (
        ("kit.icon_file", ""),
        ("kit.icon_color", ""),
        ("kit.icon_style", "classic"),
    ):
        store.set(key, value)
    assert icon.apply(info, store) is None
    assert icon.target(info).read_text() == "<svg>stock</svg>"


def test_icon_file_cannot_leave_the_folder(info):
    store = Store(info)
    store.set("kit.icon_file", "../../etc/passwd")
    assert icon.apply(info, store) is not None
