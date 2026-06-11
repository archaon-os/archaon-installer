#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing dependencies..."

if command -v pip3 >/dev/null 2>&1; then
    pip3 install -r "$SCRIPT_DIR/requirements.txt" --break-system-packages
elif command -v pip >/dev/null 2>&1; then
    pip install -r "$SCRIPT_DIR/requirements.txt" --break-system-packages
else
    echo "Error: pip not found."
    exit 1
fi

echo "Starting Archaon Installer..."

python3 "$SCRIPT_DIR/installer.py"
