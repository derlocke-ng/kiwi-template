"""The command: everything the window does, it does through the same core."""

from __future__ import annotations

import argparse
import sys

from . import APP, __version__
from .core import notes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=APP, description="Notes — the template's example app")
    parser.add_argument("--version", action="version", version=f"{APP} {__version__}")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("list", help="show the notes")
    p_add = sub.add_parser("add", help="add a note")
    p_add.add_argument("text", nargs="+")
    p_rm = sub.add_parser("remove", help="remove a note by its number")
    p_rm.add_argument("number", type=int)
    args = parser.parse_args(argv)

    try:
        if args.command == "add":
            notes.add(" ".join(args.text))
        elif args.command == "remove":
            notes.remove(args.number - 1)
        elif args.command not in (None, "list"):
            parser.error(f"unknown command {args.command}")
    except (ValueError, IndexError) as exc:
        print(f"{APP}: {exc}", file=sys.stderr)
        return 1
    for i, note in enumerate(notes.load(), 1):
        print(f"{i:3}  {note}")
    return 0
