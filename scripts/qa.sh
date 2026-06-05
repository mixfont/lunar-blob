#!/usr/bin/env bash
set -euo pipefail

mkdir -p build/reports

if command -v fontspector >/dev/null 2>&1; then
  fontspector -p googlefonts -l warn --ghmarkdown build/reports/fontspector-googlefonts.md fonts/ttf/*.ttf
else
  if ! command -v fontbakery >/dev/null 2>&1; then
    echo "fontbakery not found. Activate a venv and run: pip install -r requirements-dev.txt" >&2
    exit 127
  fi
  fontbakery check-googlefonts fonts/ttf/*.ttf --ghmarkdown build/reports/fontbakery-googlefonts.md --loglevel WARN
fi
