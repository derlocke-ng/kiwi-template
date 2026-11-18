"""The notes: ~/.local/share/kiwi-template/notes.json.

The example's data. Replace it with what your app manages; keep the shape:
plain functions, no GTK, a broken file never crashes the app.
"""

from __future__ import annotations

import json

from .. import INFO


def path():
    return INFO.data_dir() / "notes.json"


def load() -> list[str]:
    try:
        data = json.loads(path().read_text())
    except (OSError, ValueError):
        return []
    return [n for n in data if isinstance(n, str)] if isinstance(data, list) else []


def save(notes: list[str]) -> None:
    p = path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(notes, indent=2) + "\n")
    tmp.replace(p)


def add(text: str) -> list[str]:
    text = text.strip()
    if not text:
        raise ValueError("a note needs some text")
    notes = load() + [text]
    save(notes)
    return notes


def remove(index: int) -> list[str]:
    notes = load()
    if not 0 <= index < len(notes):
        raise IndexError(f"no note {index + 1}")
    del notes[index]
    save(notes)
    return notes
