#!/bin/sh
set -eu
exec python3 -B "$(dirname "$0")/runner_checkin.py" "$@"
