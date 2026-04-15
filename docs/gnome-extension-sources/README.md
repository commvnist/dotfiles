# gnome-extension-sources

Source and build workspaces for GNOME Shell extensions that should not be
stowed directly. Generated runtime files are staged into the stow package at
`gnome-extensions`.

The current component is:

- [tactiler@commvnist](tactiler@commvnist.md)

## Dependencies

Install the build and GNOME tooling:

```sh
sudo pacman -S --needed nodejs npm typescript glib2 gnome-shell make
```

No AUR package is required.

## Workflow

Build all runtime files for Tactiler and stage them into the stow package:

```sh
make -C gnome-extension-sources/tactiler@commvnist stow
```

Then stow the generated runtime package:

```sh
stow gnome-extensions
```

Enable the extension after GNOME Shell has loaded the stowed files:

```sh
gnome-extensions enable tactiler@commvnist
```
