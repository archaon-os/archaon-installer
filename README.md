# archaon-installer 🐦‍⬛

> The Archaon OS installer. Chaos is not a bug. Chaos is a feature.

archaon-installer is a fully custom TUI installer for Archaon OS. It runs on the live ISO and guides you through installing Archaon OS to your machine with a beautiful animated interface.

---

## Install

Boot from the Archaon OS live ISO and the installer launches automatically.

Or run manually on any Arch based system:

    curl -fsSL https://raw.githubusercontent.com/archaon-os/archaon-installer/main/install.sh | bash

---

## What it does

    Boot ISO
        ↓
    GRUB loads kernel
        ↓
    TTY — archaon-installer launches automatically
        ↓
    1. Welcome — ARCHAON falling animation
    2. Keyboard layout picker
    3. Timezone picker
    4. Disk selection
    5. Username and password
    6. Hostname
    7. Summary — review before installing
    8. Install — base system, grub, user setup
    9. Done — reboot

---

## Screens

**Welcome**
Animated ARCHAON logo falling in pieces from the top of the screen in neon green and blue. Full 3D shadow effect.

**Keyboard Layout**
Searchable list of keyboard layouts. Type to filter, arrow keys to navigate, ENTER to select.

**Timezone**
Searchable list of timezones. Same navigation as keyboard layout.

**Disk Selection**
Shows all available disks with size and model. Arrow keys to navigate, ENTER to select. Warns that selected disk will be wiped.

**User Setup**
Enter username, password with confirmation, and hostname.

**Summary**
Full review of all choices before installing. Press Y to confirm or N to cancel.

**Installing**
Live log of install steps as they happen.

**Done**
Press ENTER to reboot into your new Archaon OS.

---

## What gets installed

    base
    base-devel
    linux
    linux-firmware
    linux-headers
    networkmanager
    grub
    efibootmgr
    sudo
    git
    zsh
    python
    python-pip
    aon (Archaon package manager)

Hyprland and dotfiles are set up on first boot via archaon-welcome.

---

## Service

The installer runs automatically on the live ISO via systemd:

    [Unit]
    Description=Archaon OS Installer
    After=getty@tty1.service

    [Service]
    Type=idle
    ExecStart=/usr/local/bin/archaon-installer
    StandardInput=tty
    TTYPath=/dev/tty1
    User=root

    [Install]
    WantedBy=multi-user.target

---

## Requirements

- Python 3.10+
- pyfiglet
- rich
- textual
- Internet connection

All installed automatically by the bootstrap script.

---

## Part of Archaon OS 🐦‍⬛

| Repo | Purpose |
|------|---------|
| archaon-os | Main repo |
| archaon-iso | ISO build profile |
| archaon-branding | Dotfiles and assets |
| archaon-aon | Package manager |
| archaon-installer | This repo |

---

## License

GPL v3 — see LICENSE file.

---

Archaon OS — 1.0.0 "Chaotic Crow" 🐦‍⬛
