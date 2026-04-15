# dotfiles

Personal Linux dotfiles managed as GNU Stow packages.

Each top-level package directory mirrors paths relative to `$HOME`. For example,
`kitty/.config/kitty/kitty.conf` becomes `~/.config/kitty/kitty.conf` after
stowing the `kitty` package.

## Install

Install the common tooling:

```sh
sudo pacman -S --needed stow zsh kitty starship tmux vim python
```

Stow packages from the repository root:

```sh
stow zsh
stow kitty
stow starship
stow tmux
stow vim
stow scripts
stow gnome-extensions
```

Use `stow -n -v <package>` for a dry run before linking a package.

## Layout

- `gnome-extensions`: stowable GNOME Shell extension runtime files.
- `gnome-extension-sources`: source and build tooling for generated GNOME Shell
  extensions.
- `kitty`: Kitty terminal configuration.
- `scripts`: user scripts and shell functions.
- `starship`: Starship prompt configuration.
- `tmux`: tmux configuration.
- `vim`: Vim configuration.
- `zsh`: zsh shell configuration.
- `docs`: concise documentation for the repository and each package area.

## Documentation

Start with [docs/README.md](docs/README.md). Package-specific documentation is
kept under `docs/<package>/`.
