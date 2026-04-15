.PHONY: all build check clean clean-stow deps install package stow test-wayland follow-log

uuid = tactiler@commvnist
bundle = $(uuid).shell-extension.zip
stow_extension_dir = ../../gnome-extensions/.local/share/gnome-shell/extensions/$(uuid)

runtime_dirs = common extension icons preferences schemas
runtime_files = extension.js metadata.json prefs.css prefs.js stylesheet.css

all: stow

deps:
	npm ci

check: deps
	npm run check

build: check
	npm run build

stow: build
	mkdir -p $(stow_extension_dir)
	find $(stow_extension_dir) -mindepth 1 -maxdepth 1 -exec rm -rf {} +
	mkdir -p $(stow_extension_dir)
	cp -r $(addprefix build/,$(runtime_dirs)) $(stow_extension_dir)/
	cp $(addprefix build/,$(runtime_files)) $(stow_extension_dir)/
	glib-compile-schemas --strict $(stow_extension_dir)/schemas

package: build
	gnome-extensions pack --force --out-dir=. build

install: package
	gnome-extensions uninstall $(uuid) || rm -rf ~/.local/share/gnome-shell/extensions/$(uuid)/
	gnome-extensions install --force $(bundle)

clean:
	npm run clean
	rm -f $(bundle)

clean-stow:
	mkdir -p $(stow_extension_dir)
	find $(stow_extension_dir) -mindepth 1 -maxdepth 1 -exec rm -rf {} +

test-wayland:
	dbus-run-session -- gnome-shell --nested --wayland

follow-log:
	journalctl -f /usr/bin/gnome-shell
