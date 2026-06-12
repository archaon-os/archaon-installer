#!/bin/bash
# archaon-installer bootstrap
# curl -fsSL https://raw.githubusercontent.com/archaon-os/archaon-installer/main/install.sh | bash

GREEN='\033[38;2;0;255;136m'
BLUE='\033[38;2;0;204;255m'
DIM='\033[38;2;51;51;51m'
RED='\033[38;2;255;0;85m'
RESET='\033[0m'
BOLD='\033[1m'

crow_log() {
    echo -e "${BLUE}  🐦‍⬛  $1${RESET}"
    sleep 0.6
}

error() {
    echo -e "${RED}  ✗ $1${RESET}"
    exit 1
}

success() {
    echo -e "${GREEN}  ✓ $1${RESET}"
}

echo -e "${GREEN}"
echo "        /\\"
echo "       /  \\"
echo "      / /\\ \\"
echo "     / /  \\ \\"
echo "    / / /\\ \\ \\"
echo "   /_/ /__\\ \\_\\"
echo -e "${BLUE}      /\\  /\\"
echo "     /  \\/  \\"
echo "     \\  /\\  /"
echo -e "      \\/  \\/${RESET}"
echo ""
echo -e "  ${GREEN}${BOLD}A R C H A O N  O S${RESET}"
echo -e "  ${BLUE}Archaon OS Installer v0.1.0 — Chaotic Crow 🐦‍⬛${RESET}"
echo ""

# ─────────────────────────────────────────
# CHECK ROOT
# ─────────────────────────────────────────

if [ "$EUID" -ne 0 ]; then
    error "Please run as root: sudo bash install.sh"
fi

# ─────────────────────────────────────────
# DETECT PACKAGE MANAGER
# ─────────────────────────────────────────

crow_log "Detecting system..."

if command -v pacman &>/dev/null; then
    PKG_MANAGER="pacman"
    crow_log "Found Arch Linux / pacman"
elif command -v apt &>/dev/null; then
    PKG_MANAGER="apt"
    crow_log "Found Debian / apt"
elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
    crow_log "Found Fedora / dnf"
else
    error "Unsupported package manager. Archaon installer requires Arch, Debian, or Fedora based systems."
fi

# ─────────────────────────────────────────
# INSTALL PYTHON
# ─────────────────────────────────────────

crow_log "Checking Python..."

if ! command -v python3 &>/dev/null; then
    crow_log "Installing Python..."
    case $PKG_MANAGER in
        pacman) pacman -S --noconfirm python python-pip ;;
        apt)    apt-get install -y python3 python3-pip ;;
        dnf)    dnf install -y python3 python3-pip ;;
    esac
    success "Python installed"
else
    PY_VERSION=$(python3 --version 2>&1)
    success "Python found: $PY_VERSION"
fi

# ─────────────────────────────────────────
# INSTALL PIP
# ─────────────────────────────────────────

crow_log "Checking pip..."

if ! command -v pip3 &>/dev/null && ! python3 -m pip --version &>/dev/null; then
    crow_log "Installing pip..."
    case $PKG_MANAGER in
        pacman) pacman -S --noconfirm python-pip ;;
        apt)    apt-get install -y python3-pip ;;
        dnf)    dnf install -y python3-pip ;;
    esac
    success "pip installed"
else
    success "pip found"
fi

# ─────────────────────────────────────────
# INSTALL CURL IF MISSING
# ─────────────────────────────────────────

if ! command -v curl &>/dev/null; then
    crow_log "Installing curl..."
    case $PKG_MANAGER in
        pacman) pacman -S --noconfirm curl ;;
        apt)    apt-get install -y curl ;;
        dnf)    dnf install -y curl ;;
    esac
fi

# ─────────────────────────────────────────
# INSTALL PYTHON DEPS
# ─────────────────────────────────────────

crow_log "Pecking at dependencies..."

install_pip_pkg() {
    python3 -m pip install "$1" --break-system-packages -q 2>/dev/null || \
    python3 -m pip install "$1" -q 2>/dev/null || \
    pip3 install "$1" --break-system-packages -q 2>/dev/null || \
    pip3 install "$1" -q 2>/dev/null
}

crow_log "Installing pyfiglet..."
install_pip_pkg pyfiglet
success "pyfiglet ready"

crow_log "Installing rich..."
install_pip_pkg rich
success "rich ready"

crow_log "Installing textual..."
install_pip_pkg textual
success "textual ready"

crow_log "Installing requests..."
install_pip_pkg requests
success "requests ready"

# ─────────────────────────────────────────
# DOWNLOAD INSTALLER
# ─────────────────────────────────────────

crow_log "Stealing the installer from GitHub..."

INSTALLER_URL="https://raw.githubusercontent.com/archaon-os/archaon-installer/main/installer.py"
INSTALLER_PATH="/tmp/archaon-installer.py"

if ! curl -fsSL "$INSTALLER_URL" -o "$INSTALLER_PATH"; then
    error "Failed to download installer. Check your internet connection."
fi

success "Installer downloaded"
chmod +x "$INSTALLER_PATH"

# ─────────────────────────────────────────
# RUN INSTALLER
# ─────────────────────────────────────────

crow_log "Waking up the crow..."
sleep 1

echo ""
echo -e "  ${GREEN}Launching Archaon OS Installer...${RESET}"
echo ""
sleep 0.5

python3 "$INSTALLER_PATH"

# ─────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────

rm -f "$INSTALLER_PATH"
