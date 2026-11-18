#!/usr/bin/env bash
# check-version.sh — the version is written in three places; they must agree.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
m="$(sed -n 's/^VERSION=//p' kiwi.manifest)"
p="$(sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml | head -1)"
i="$(sed -n 's/^__version__ = "\(.*\)"/\1/p' src/*/__init__.py | head -1)"
for other in "$p" "$i"; do
    if [[ $other != "$m" ]]; then
        echo "check-version: kiwi.manifest=$m pyproject.toml=$p __init__.py=$i" >&2
        exit 1
    fi
done
echo "check-version: ok ($m)"
