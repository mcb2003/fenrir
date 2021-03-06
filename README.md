# Fenrir
A modern, modular, flexible and fast console screenreader.
It should run on any operating system. If you want to help, or write drivers to make it work on other systems, just let me know. 
This software is licensed under the LGPL v3.

# OS Requirements
- Linux (ptyDriver, vcsaDriver, evdevDriver)
- macOS (ptyDriver)
- BSD (ptyDriver)
- Windows (ptyDriver)

# Core Requirements
- python3 >= 3.3
- screen, input, speech, sound or braille drivers dependencies see "Features, Drivers, Extras".

# Features, Drivers, Extras, Dependencies
# Input Drivers:
1. "evdevDriver" input driver for linux evdev
  - python-evdev >=0.6.3 (This is commonly referred to as python3-evdev by your distribution)
  - python-pyudev
  - loaded uinput kernel module
  - ReadWrite permission 
    - /dev/input
    - /dev/uinput
2. "ptyDriver" terminal emulation input driver
  - python-pyte

# Screen Drivers:
1. "vcsaDriver" screen driver for linux VCSA devices
  - python-dbus
  - Read permission to the following files and services:
    - /sys/devices/virtual/tty/tty0/active
    - /dev/tty[1-64]
    - /dev/vcsa[1-64]
    - read logind DBUS
2. "ptyDriver" terminal emulation driver
  - python-pyte
  
# Speech Drivers:
1. "genericDriver" (default) speech driver for sound as subprocess:
  - espeak or espeak-ng
2. "espeakDriver" speech driver for Espeak or Espeak-NG:
  - python-espeak
3. "speechdDriver" speech driver for Speech-dispatcher:
  - Speech-dispatcher
  - python-speechd
4. "emacspeakDriver" speech driver for emacspeak
  - emacspeak

# Braille Drivers:
1. "BrlttyDriver" braille driver (WIP):
  - brltty (configured and running)
  - python-brlapi

# Sound Drivers:
1. "genericDriver" (default) sound driver for sound as subprocess:
  - Sox
2. "gstreamerDriver" sound driver for gstreamer
  - gstreamer >=1.0
  - GLib

# Extras:
1. spellchecker
  - python-pyenchant
  - aspell-YourLanguageCode (example aspell-en for us English)
2. Unix daemon (also needed for Systemd):
  - python-daemonize
3. Modify system volume:
  - pyalsaaudio (needs libasound2's headers).

# installation
- Archlinux: PKGBUILD in AUR
- PIP: sudo pip install fenrir-screenreader
- Manual:
 - install "espeak" and "sox" with your package manager
 - sudo pip install -r requirements.txt 
 - run install.sh and uninstall.sh as root
- you also can just run it from Git without installing:
You can just run the following as root:
if you are in Fenrir Git rootfolder:
cd src/fenrir/
sudo ./fenrir
Settings "settings.conf" is located in the "config" directory or after installation in /etc/fenrir/settings.
Take care to use drivers from the config matching your installed drivers. 
By default it uses:
- sound driver: genericDriver (via sox, could configured in settings.conf)
- speech driver: genericDriver (via espeak or espeak-ng, could configured in settings.conf)
- braille driver: brlttyDriver (WIP)
- input driver: evdevDriver

# Documentation
You can see all information on the Wiki:
https://wiki.linux-a11y.org/doku.php?id=fenrir_user_manual
