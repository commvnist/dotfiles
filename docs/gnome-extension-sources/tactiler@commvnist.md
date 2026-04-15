# tactiler@commvnist

TypeScript source for `tactiler@commvnist`, a fork of Tactile by Lasse Lundal.
The source lives outside the stowed GNOME extension package so development files
do not get linked into `~/.local/share/gnome-shell/extensions`.

## Source Layout

- `src/extension.ts`: GNOME Shell extension entry point.
- `src/extension/`: modal UI and shell utility code.
- `src/common/`: layout, area, array, and style helpers shared by extension and
  preferences code.
- `src/preferences/`: preferences UI pages and input widgets.
- `src/schemas/`: GSettings schema.
- `icons/`: extension icons copied into the runtime build.
- `Makefile`: build, stage, package, and install commands.

## Dependencies

```sh
sudo pacman -S --needed nodejs npm typescript glib2 gnome-shell make
```

No AUR package is required.

## Commands

Run checks:

```sh
make -C gnome-extension-sources/tactiler@commvnist check
```

Build TypeScript into `build/`:

```sh
make -C gnome-extension-sources/tactiler@commvnist build
```

Stage loadable runtime files into the stow package:

```sh
make -C gnome-extension-sources/tactiler@commvnist stow
```

Create a `.shell-extension.zip` bundle:

```sh
make -C gnome-extension-sources/tactiler@commvnist package
```

Clean local build output:

```sh
make -C gnome-extension-sources/tactiler@commvnist clean
```

## Staged Output

`make stow` writes only GNOME-loadable files into:

```sh
gnome-extensions/.local/share/gnome-shell/extensions/tactiler@commvnist
```

That directory is safe to link with:

```sh
stow gnome-extensions
```
