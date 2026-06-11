#!/usr/bin/env python3
"""
archaon-installer
Version: 0.1.0 "Chaotic Crow"
Archaon OS Installer
"""

import os
import sys
import time
import random
import subprocess
import tty
import termios
from pathlib import Path

import pyfiglet
from rich.console import Console

console = Console()

# ─────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────

GREEN = '\033[38;2;0;255;136m'
BLUE = '\033[38;2;0;204;255m'
DIM = '\033[38;2;51;51;51m'
RED = '\033[38;2;255;0;85m'
YELLOW = '\033[38;2;255;170;0m'
RESET = '\033[0m'
BOLD = '\033[1m'

GLITCH = ['░', '▒', '▓', '█', '▄', '▀', '■', '●']

# ─────────────────────────────────────────
# LOGO GENERATOR
# ─────────────────────────────────────────

def get_logo(word='ARCHAON'):
    text = pyfiglet.figlet_format(word, font='colossal')
    lines = text.split('\n')
    max_len = max(len(l) for l in lines)
    result = []
    for i, line in enumerate(lines):
        padded = line.ljust(max_len + 2)
        new_line = ''
        for j, ch in enumerate(padded):
            if ch != ' ':
                new_line += ch
            else:
                if i > 0 and j > 0 and j-1 < len(lines[i-1]) and lines[i-1][j-1] != ' ':
                    new_line += '░'
                else:
                    new_line += ' '
        result.append(new_line)
    return result

# ─────────────────────────────────────────
# WELCOME ANIMATION
# ─────────────────────────────────────────

def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 120, 40

def welcome_animation():
    logo = get_logo('ARCHAON')
    cols, rows = get_terminal_size()
    logo_height = len(logo)
    logo_width = max(len(l) for l in logo)
    left_pad = max(0, (cols - logo_width) // 2)

    line_pos = []
    line_speed = []
    for i in range(logo_height):
        line_pos.append(-(logo_height - i) - random.randint(0, 8))
        line_speed.append(round(random.uniform(0.3, 0.9), 1))

    final_top = max(0, (rows - logo_height - 6) // 2)
    final_positions = [final_top + i for i in range(logo_height)]
    landed = [False] * logo_height

    while not all(landed):
        os.system('clear')
        for i in range(logo_height):
            if not landed[i]:
                line_pos[i] += line_speed[i]
                if line_pos[i] >= final_positions[i]:
                    line_pos[i] = final_positions[i]
                    landed[i] = True

        frame_lines = {}
        for i in range(logo_height):
            y = int(line_pos[i])
            if y >= 0:
                frame_lines[y] = (logo[i], landed[i])

        for y in range(rows - 4):
            if y in frame_lines:
                line, is_landed = frame_lines[y]
                out = ' ' * left_pad
                for ch in line:
                    if ch == '░':
                        out += BLUE + ch + RESET
                    elif ch != ' ':
                        if is_landed:
                            out += GREEN + ch + RESET
                        else:
                            out += YELLOW + ch + RESET
                    else:
                        out += ' '
                print(out)
            else:
                print()
        time.sleep(0.04)

    # Flash effect
    for _ in range(3):
        os.system('clear')
        for i in range(rows - 4):
            if i in range(final_top, final_top + logo_height):
                idx = i - final_top
                out = ' ' * left_pad
                for ch in logo[idx]:
                    if ch == '░':
                        out += BLUE + ch + RESET
                    elif ch != ' ':
                        out += BOLD + GREEN + ch + RESET
                    else:
                        out += ' '
                print(out)
            else:
                print()
        time.sleep(0.08)

        os.system('clear')
        for i in range(rows - 4):
            if i in range(final_top, final_top + logo_height):
                idx = i - final_top
                out = ' ' * left_pad
                for ch in logo[idx]:
                    if ch == '░':
                        out += BLUE + ch + RESET
                    elif ch != ' ':
                        out += GREEN + ch + RESET
                    else:
                        out += ' '
                print(out)
            else:
                print()
        time.sleep(0.08)

    subtitle = "A R C H A O N  O S"
    sub2 = "Archaon OS Installer v0.1.0 — Chaotic Crow 🐦‍⬛"
    print()
    print(' ' * ((cols - len(subtitle)) // 2) + GREEN + BOLD + subtitle + RESET)
    print(' ' * ((cols - len(sub2)) // 2) + BLUE + sub2 + RESET)
    print()
    time.sleep(1.5)

# ─────────────────────────────────────────
# KEYBOARD LAYOUT
# ─────────────────────────────────────────

KEYBOARD_LAYOUTS = [
    "us", "uk", "de", "fr", "es", "it", "pt", "ru", "jp", "kr",
    "cn", "ar", "tr", "pl", "nl", "se", "no", "dk", "fi", "cz",
    "sk", "hu", "ro", "bg", "hr", "sr", "sl", "lt", "lv", "et",
    "gr", "he", "th", "vi", "id", "ms", "ua", "by", "az", "ge",
    "am", "ka", "br", "mx", "ca", "au", "nz", "za", "in", "pk",
]

def keyboard_screen():
    search = ""
    selected_idx = 0

    while True:
        filtered = [k for k in KEYBOARD_LAYOUTS if search.lower() in k.lower()]
        cols, _ = get_terminal_size()

        os.system('clear')
        print()
        print(' ' * ((cols - 40) // 2) + GREEN + BOLD + "── Keyboard Layout ──" + RESET)
        print()
        print(' ' * ((cols - 40) // 2) + BLUE + f"Search: {GREEN}{search}▌{RESET}")
        print()

        display = filtered[:15]
        for i, layout in enumerate(display):
            prefix = f"  {GREEN}▶{RESET} " if i == selected_idx else "    "
            color = GREEN if i == selected_idx else DIM
            print(' ' * ((cols - 40) // 2) + prefix + color + layout + RESET)

        print()
        print(' ' * ((cols - 40) // 2) + DIM + "↑↓ Navigate  |  ENTER — Select  |  BACKSPACE — Delete" + RESET)

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        if ch == '\r' or ch == '\n':
            if filtered:
                return filtered[selected_idx]
        elif ch == '\x7f':
            search = search[:-1]
            selected_idx = 0
        elif ch == '\x1b':
            next1 = sys.stdin.read(1)
            next2 = sys.stdin.read(1)
            if next1 == '[':
                if next2 == 'A' and selected_idx > 0:
                    selected_idx -= 1
                elif next2 == 'B' and selected_idx < len(filtered) - 1:
                    selected_idx += 1
        elif ch.isprintable():
            search += ch
            selected_idx = 0

# ─────────────────────────────────────────
# TIMEZONE
# ─────────────────────────────────────────

TIMEZONES = [
    "Africa/Cairo", "Africa/Johannesburg", "Africa/Lagos",
    "America/Chicago", "America/Los_Angeles", "America/New_York",
    "America/Sao_Paulo", "America/Toronto", "America/Vancouver",
    "Asia/Bangalore", "Asia/Bangkok", "Asia/Beirut", "Asia/Dubai",
    "Asia/Hong_Kong", "Asia/Jakarta", "Asia/Karachi", "Asia/Kolkata",
    "Asia/Kuwait", "Asia/Manila", "Asia/Riyadh", "Asia/Seoul",
    "Asia/Shanghai", "Asia/Singapore", "Asia/Tehran", "Asia/Tokyo",
    "Australia/Melbourne", "Australia/Perth", "Australia/Sydney",
    "Europe/Amsterdam", "Europe/Athens", "Europe/Berlin",
    "Europe/Brussels", "Europe/Bucharest", "Europe/Budapest",
    "Europe/Copenhagen", "Europe/Dublin", "Europe/Helsinki",
    "Europe/Istanbul", "Europe/Kiev", "Europe/Lisbon", "Europe/London",
    "Europe/Luxembourg", "Europe/Madrid", "Europe/Moscow",
    "Europe/Oslo", "Europe/Paris", "Europe/Prague", "Europe/Rome",
    "Europe/Sofia", "Europe/Stockholm", "Europe/Vienna",
    "Europe/Warsaw", "Europe/Zurich", "Pacific/Auckland",
    "Pacific/Honolulu", "UTC",
]

def timezone_screen():
    search = ""
    selected_idx = 0

    while True:
        filtered = [t for t in TIMEZONES if search.lower() in t.lower()]
        cols, _ = get_terminal_size()

        os.system('clear')
        print()
        print(' ' * ((cols - 40) // 2) + GREEN + BOLD + "── Timezone ──" + RESET)
        print()
        print(' ' * ((cols - 40) // 2) + BLUE + f"Search: {GREEN}{search}▌{RESET}")
        print()

        display = filtered[:15]
        for i, tz in enumerate(display):
            prefix = f"  {GREEN}▶{RESET} " if i == selected_idx else "    "
            color = GREEN if i == selected_idx else DIM
            print(' ' * ((cols - 40) // 2) + prefix + color + tz + RESET)

        print()
        print(' ' * ((cols - 40) // 2) + DIM + "↑↓ Navigate  |  ENTER — Select  |  BACKSPACE — Delete" + RESET)

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        if ch == '\r' or ch == '\n':
            if filtered:
                return filtered[selected_idx]
        elif ch == '\x7f':
            search = search[:-1]
            selected_idx = 0
        elif ch == '\x1b':
            next1 = sys.stdin.read(1)
            next2 = sys.stdin.read(1)
            if next1 == '[':
                if next2 == 'A' and selected_idx > 0:
                    selected_idx -= 1
                elif next2 == 'B' and selected_idx < len(filtered) - 1:
                    selected_idx += 1
        elif ch.isprintable():
            search += ch
            selected_idx = 0

# ─────────────────────────────────────────
# DISK SELECTION
# ─────────────────────────────────────────

def get_disks():
    output = subprocess.run(
        "lsblk -d -o NAME,SIZE,MODEL --noheadings | grep -v loop",
        shell=True, capture_output=True, text=True
    ).stdout.strip()
    disks = []
    for line in output.split('\n'):
        if line.strip():
            parts = line.split()
            name = parts[0]
            size = parts[1] if len(parts) > 1 else "?"
            model = ' '.join(parts[2:]) if len(parts) > 2 else "Unknown"
            disks.append((f"/dev/{name}", size, model))
    return disks

def disk_screen():
    disks = get_disks()
    selected_idx = 0
    cols, _ = get_terminal_size()

    while True:
        os.system('clear')
        print()
        print(' ' * ((cols - 40) // 2) + GREEN + BOLD + "── Select Disk ──" + RESET)
        print(' ' * ((cols - 40) // 2) + RED + "⚠  Selected disk will be WIPED" + RESET)
        print()

        for i, (name, size, model) in enumerate(disks):
            prefix = f"  {GREEN}▶{RESET} " if i == selected_idx else "    "
            color = GREEN if i == selected_idx else DIM
            print(' ' * ((cols - 40) // 2) + prefix + color + f"{name:<12} {size:<8} {model}" + RESET)

        print()
        print(' ' * ((cols - 40) // 2) + DIM + "↑↓ Navigate  |  ENTER — Select" + RESET)

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        if ch == '\r' or ch == '\n':
            if disks:
                return disks[selected_idx][0]
        elif ch == '\x1b':
            next1 = sys.stdin.read(1)
            next2 = sys.stdin.read(1)
            if next1 == '[':
                if next2 == 'A' and selected_idx > 0:
                    selected_idx -= 1
                elif next2 == 'B' and selected_idx < len(disks) - 1:
                    selected_idx += 1

# ─────────────────────────────────────────
# USER SETUP
# ─────────────────────────────────────────

def input_screen(title, prompt, secret=False):
    cols, _ = get_terminal_size()
    os.system('clear')
    print()
    print(' ' * ((cols - 40) // 2) + GREEN + BOLD + f"── {title} ──" + RESET)
    print()
    print(' ' * ((cols - 40) // 2) + BLUE + prompt + RESET)
    print(' ' * ((cols - 40) // 2), end='')

    if secret:
        import getpass
        return getpass.getpass('')
    else:
        return input()

def user_screen():
    username = input_screen("Create User", "Enter username: ")
    while True:
        password = input_screen("Create User", "Enter password: ", secret=True)
        confirm = input_screen("Create User", "Confirm password: ", secret=True)
        if password == confirm:
            break
        cols, _ = get_terminal_size()
        print(' ' * ((cols - 40) // 2) + RED + "Passwords don't match, try again." + RESET)
        time.sleep(1)
    hostname = input_screen("Hostname", "Enter hostname (default: archaon): ")
    if not hostname.strip():
        hostname = "archaon"
    return username.strip(), password, hostname.strip()

# ─────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────

def summary_screen(kb, tz, disk, username, hostname):
    cols, _ = get_terminal_size()

    while True:
        os.system('clear')
        print()
        print(' ' * ((cols - 40) // 2) + GREEN + BOLD + "── Installation Summary ──" + RESET)
        print()
        pad = ' ' * ((cols - 40) // 2)
        print(pad + BLUE + f"  Keyboard:  {GREEN}{kb}{RESET}")
        print(pad + BLUE + f"  Timezone:  {GREEN}{tz}{RESET}")
        print(pad + BLUE + f"  Disk:      {RED}{disk} ← WILL BE WIPED{RESET}")
        print(pad + BLUE + f"  Username:  {GREEN}{username}{RESET}")
        print(pad + BLUE + f"  Hostname:  {GREEN}{hostname}{RESET}")
        print()
        print(pad + YELLOW + "  ⚠  This will erase all data on " + disk + RESET)
        print()
        print(pad + GREEN + "  [Y] Confirm and install" + RESET)
        print(pad + RED + "  [N] Cancel" + RESET)
        print()

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        if ch.lower() == 'y':
            return True
        elif ch.lower() == 'n':
            return False

# ─────────────────────────────────────────
# INSTALLER
# ─────────────────────────────────────────

def log(msg, color=GREEN):
    cols, _ = get_terminal_size()
    print(' ' * ((cols - 60) // 2) + color + f"  → {msg}" + RESET)

def install(kb, tz, disk, username, password, hostname):
    cols, _ = get_terminal_size()
    os.system('clear')
    print()
    print(' ' * ((cols - 40) // 2) + GREEN + BOLD + "── Installing Archaon OS ──" + RESET)
    print()

    # Detect nvme
    efi = f"{disk}1" if "nvme" not in disk else f"{disk}p1"
    root = f"{disk}2" if "nvme" not in disk else f"{disk}p2"

    steps = [
        ("Wiping disk...", f"wipefs -af {disk}"),
        ("Partitioning...", f"parted -s {disk} mklabel gpt mkpart ESP fat32 1MiB 513MiB set 1 esp on mkpart ROOT ext4 513MiB 100%"),
        ("Formatting EFI...", f"mkfs.fat -F32 {efi}"),
        ("Formatting root...", f"mkfs.ext4 -F {root}"),
        ("Mounting partitions...", f"mount {root} /mnt && mkdir -p /mnt/boot/efi && mount {efi} /mnt/boot/efi"),
        ("Installing base system...", "pacstrap -K /mnt base base-devel linux linux-firmware linux-headers networkmanager grub efibootmgr sudo git zsh python python-pip"),
        ("Generating fstab...", "genfstab -U /mnt >> /mnt/etc/fstab"),
    ]

    for msg, cmd in steps:
        log(msg)
        subprocess.run(cmd, shell=True, capture_output=True)

    log("Configuring system...")
    chroot_cmds = f"""
ln -sf /usr/share/zoneinfo/{tz} /etc/localtime
hwclock --systohc
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
echo "{hostname}" > /etc/hostname
echo "127.0.1.1 {hostname}.localdomain {hostname}" >> /etc/hosts
echo "{kb}" > /etc/vconsole.conf
mkinitcpio -P
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ARCHAON --removable
grub-mkconfig -o /boot/grub/grub.cfg
useradd -m -G wheel,audio,video,storage -s /bin/zsh {username}
echo "{username}:{password}" | chpasswd
echo "root:{password}" | chpasswd
echo "%wheel ALL=(ALL:ALL) ALL" >> /etc/sudoers
systemctl enable NetworkManager
"""
    subprocess.run(f"arch-chroot /mnt /bin/bash -c '{chroot_cmds}'", shell=True)

    log("Setting up Archaon identity...")
    subprocess.run("""cat > /mnt/etc/os-release << 'EOF'
NAME="Archaon OS"
PRETTY_NAME="Archaon OS 1.0.0 Chaotic Crow"
ID=archaon
ID_LIKE=arch
BUILD_ID=rolling
ANSI_COLOR="1;32"
HOME_URL="https://github.com/archaon-os"
LOGO=archaon
EOF""", shell=True)

    log("Installing aon package manager...")
    subprocess.run(f"""arch-chroot /mnt /bin/bash -c '
curl -fsSL https://raw.githubusercontent.com/archaon-os/archaon-aon/main/install.sh | bash
'""", shell=True)

    log("Unmounting...")
    subprocess.run("umount -R /mnt", shell=True)

    print()
    print(' ' * ((cols - 40) // 2) + GREEN + BOLD + "✓ Installation complete!" + RESET)
    print(' ' * ((cols - 40) // 2) + BLUE + "Remove the USB and reboot." + RESET)
    print()

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():
    try:
        import pyfiglet
    except ImportError:
        subprocess.call("pip install pyfiglet rich --break-system-packages -q", shell=True)

    welcome_animation()

    cols, _ = get_terminal_size()
    print(' ' * ((cols - 40) // 2) + GREEN + "Press ENTER to begin installation..." + RESET)
    input()

    kb = keyboard_screen()
    tz = timezone_screen()
    disk = disk_screen()
    username, password, hostname = user_screen()

    confirmed = summary_screen(kb, tz, disk, username, hostname)
    if not confirmed:
        print(f"\n  {RED}Installation cancelled.{RESET}\n")
        sys.exit(0)

    install(kb, tz, disk, username, password, hostname)

    print(f"  {GREEN}Press ENTER to reboot...{RESET}")
    input()
    subprocess.run("reboot", shell=True)

if __name__ == "__main__":
    main()