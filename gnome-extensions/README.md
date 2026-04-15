# GNOME extensions

This is a GNU Stow package for local GNOME Shell extensions.

## Syswatch

Stow the package from the repository root:

```sh
stow gnome-extensions
```

Then reload GNOME Shell or log out and back in, and enable the extension:

```sh
gnome-extensions enable syswatch@commvnist
gnome-extensions enable netwatch@commvnist
gnome-extensions enable tactiler@commvnist
```

The extension adds a compact top-bar monitor for CPU usage/temp/frequency, GPU
usage/temp, and RAM usage. Numeric fields are padded and monospace so updates do
not resize the widget.

Clicking the widget opens `kitty` and starts `syswatch`.

The network extension sits on the left side of the top bar and shows the local
IPv4 address plus download and upload speeds.

## Tactiler

Tactiler is built from `gnome-extension-sources/tactiler@commvnist`.

To rebuild the stowable extension directory:

```sh
make -C gnome-extension-sources/tactiler@commvnist stow
```

That command compiles the TypeScript source and stages only the GNOME-loadable
runtime files into `.local/share/gnome-shell/extensions/tactiler@commvnist`.
