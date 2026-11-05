#!/bin/sh
# Local-only browser batch. Installs nothing; no personal profile or public action.
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if [ -z "${CHROME_PATH:-}" ]; then
  for candidate in "$HOME/Library/Caches/ms-playwright"/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell; do
    if [ -x "$candidate" ]; then CHROME_PATH="$candidate"; export CHROME_PATH; break; fi
  done
fi
node scripts/browser-check.mjs
