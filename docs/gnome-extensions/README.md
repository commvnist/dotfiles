# gnome-extensions

GNU Stow package for local GNOME Shell extension runtime files. This directory
is meant to be linked into `$HOME` with Stow.

## Dependencies

Runtime:

```sh
sudo pacman -S --needed gnome-shell zsh kitty
```

Build dependencies for generated extensions are documented under
[gnome-extension-sources](../gnome-extension-sources/README.md).

No AUR package is required.

## Install

From the repository root:

```sh
stow gnome-extensions
```

Reload GNOME Shell or log out and back in, then enable extensions:

```sh
gnome-extensions enable syswatch@commvnist
gnome-extensions enable netwatch@commvnist
gnome-extensions enable tactiler@commvnist
```

## Components

- `syswatch@commvnist`: top-bar system monitor launcher/summary.
- `netwatch@commvnist`: top-bar IPv4 and network throughput indicator.
- `tactiler@commvnist`: generated runtime for Tactiler.

Tactiler should be regenerated from source with:

```sh
make -C gnome-extension-sources/tactiler@commvnist stow
```
