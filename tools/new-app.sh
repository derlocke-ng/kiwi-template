#!/usr/bin/env bash
# new-app.sh — turn a copy of kiwi-template into your app.
#
#   tools/new-app.sh kiwi-notes "Kiwi Notes" eu.kiwinetwork.KiwiNotes [github-user]
#
#   kiwi-notes                 the command and repository name (lower case, dashes)
#   "Kiwi Notes"               the name as the UI writes it
#   eu.kiwinetwork.KiwiNotes   the application id (reverse DNS of a domain you own)
#   github-user                where the repository lives; default derlocke-ng
#
# Run it once, in a fresh copy ("Use this template" on GitHub, then clone).
# It renames the package, the data files and every mention, and resets the
# version to 0.1.0. The kit (src/<package>/kit) is not touched.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
[[ $# -ge 3 ]] || { sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
app="$1" name="$2" id="$3" user="${4:-derlocke-ng}"
[[ $app =~ ^[a-z][a-z0-9-]*$ ]] || { echo "new-app: '$app' — lower case letters, digits and dashes" >&2; exit 1; }
[[ $id =~ ^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+$ ]] || { echo "new-app: '$id' is not an application id" >&2; exit 1; }
[[ -d src/kiwi_template ]] || { echo "new-app: already renamed (no src/kiwi_template)" >&2; exit 1; }
pkg="${app//-/_}"

git mv src/kiwi_template "src/$pkg" 2>/dev/null || mv src/kiwi_template "src/$pkg"
for ext in desktop svg; do
    git mv "data/eu.kiwinetwork.KiwiTemplate.$ext" "data/$id.$ext" 2>/dev/null \
        || mv "data/eu.kiwinetwork.KiwiTemplate.$ext" "data/$id.$ext"
done
# every text file except the kit, the docs about the template itself, and git
grep -rIl -e kiwi-template -e kiwi_template -e KiwiTemplate -e 'Kiwi Template' \
        --exclude-dir=.git --exclude-dir=kit --exclude-dir=docs --exclude=new-app.sh --exclude=kit-update.sh . \
    | while read -r f; do
        sed -i \
            -e "s|derlocke-ng/kiwi-template|$user/$app|g" \
            -e "s|eu\.kiwinetwork\.KiwiTemplate|$id|g" \
            -e "s|kiwi_template|$pkg|g" \
            -e "s|kiwi-template|$app|g" \
            -e "s|Kiwi Template|$name|g" "$f"
    done
echo "new-app: this is now $app ($name, $id)"
echo "  next: write your own README.md and docs/, replace data/$id.svg,"
echo "        replace core/notes.py and ui/window.py with your app, then: make check"
