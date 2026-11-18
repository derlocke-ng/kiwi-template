import pytest

from kiwi_template import cli
from kiwi_template.core import notes


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))


def test_add_list_remove(capsys):
    assert cli.main(["add", "buy", "milk"]) == 0
    assert notes.load() == ["buy milk"]
    assert cli.main(["remove", "1"]) == 0
    assert notes.load() == []
    assert cli.main(["remove", "5"]) == 1


def test_broken_file_is_an_empty_list():
    notes.path().parent.mkdir(parents=True, exist_ok=True)
    notes.path().write_text("nope")
    assert notes.load() == []
