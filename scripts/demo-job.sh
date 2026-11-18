#!/usr/bin/env bash
# demo-job.sh — the example's bash part: a job in steps, as an app's real work
# (a build, a sync, a container start) would print them. The window runs it
# through the kit's job strip and counts the "step" lines.
set -euo pipefail
steps="${1:-4}"
for i in $(seq 1 "$steps"); do
    echo ":: working on part $i"
    sleep "${DEMO_STEP_SECONDS:-1}"
    echo "step $i of $steps done"
done
[[ "${DEMO_FAIL:-0}" == 1 ]] && { echo "error: the demo was asked to fail" >&2; exit 1; }
echo ":: all done"
