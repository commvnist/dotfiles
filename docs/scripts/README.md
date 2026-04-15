# scripts

GNU Stow package for user scripts and shell helpers under `~/.scripts`.

## Components

- `syswatch.zsh`: interactive hardware monitor zsh function.
- `obsidian_movie_entry.py`: creates an Obsidian movie note from TMDB data.
- `obsidian_movie_entry.zsh`: zsh wrapper for the movie-entry script.

## Dependencies

Base:

```sh
sudo pacman -S --needed zsh python
```

Optional for `syswatch`:

```sh
sudo pacman -S --needed nvidia-utils
```

No AUR package is required by these scripts.

## Install

From the repository root:

```sh
stow scripts
```

## Usage

`syswatch` is available when `.zshrc` sources the stowed script functions.

`syswatch` can read Intel RAPL energy counters for CPU package power. Those
sysfs files are root-owned by default. To allow read access through a dedicated
group:

```sh
sudo groupadd --system rapl
sudo usermod -aG rapl "$USER"
echo 'z /sys/class/powercap/intel-rapl:0/energy_uj 0440 root rapl -' | sudo tee /etc/tmpfiles.d/rapl.conf
sudo systemd-tmpfiles --create /etc/tmpfiles.d/rapl.conf
```

Log out and back in after changing group membership.

Movie note creation uses TMDB HTML and writes to
`$OBSIDIAN_MOVIES_DIR`, defaulting to `~/Documents/naek/movies`.
