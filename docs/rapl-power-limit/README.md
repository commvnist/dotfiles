# RAPL Power Limit

`rapl-power-limit` stores the ThinkPad P16 Gen 2 MMIO RAPL restore tooling in this repository. It restores the CPU package MMIO RAPL limits and can monitor those limits for later firmware or platform rewrites.

The package exists because this host has been observed entering a platform state where CPU package power is held around 25 W even though temperatures are low and normal performance settings are active. The immediate cause is a low MMIO-backed RAPL long-term package limit. The monitor service handles the related case where the platform rewrites that limit again after the initial restore.

## Files

- `rapl-power-limit/usr/local/sbin/restore-cpu-rapl-limits`
- `rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits.service`
- `rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits-monitor.service`
- `rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits-resume.service`
- `rapl-power-limit/usr/share/doc/system/rapl-power-limit.md`

This package targets `/`, not `$HOME`, because it installs machine-level files under `/etc`, `/usr/local`, and `/usr/share`. The live install should use real root-owned files, not stowed symlinks into this repository. PID 1 can load enabled units before `/home` is mounted, and `/home`-backed unit symlinks can therefore fail at boot with `Failed to open ... No such file or directory`.

## Install

Run commands from the repository root:

```sh
cd /home/naek/system
```

If an older copy was stowed into `/`, remove the generated systemd enablement
links and unstow the package first:

```sh
sudo systemctl disable --now restore-cpu-rapl-limits-monitor.service
sudo systemctl disable restore-cpu-rapl-limits.service restore-cpu-rapl-limits-resume.service
sudo stow --delete --target=/ rapl-power-limit
```

Install real files onto the root filesystem:

```sh
sudo install -D -m 0755 rapl-power-limit/usr/local/sbin/restore-cpu-rapl-limits /usr/local/sbin/restore-cpu-rapl-limits
sudo install -D -m 0644 rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits.service /etc/systemd/system/restore-cpu-rapl-limits.service
sudo install -D -m 0644 rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits-monitor.service /etc/systemd/system/restore-cpu-rapl-limits-monitor.service
sudo install -D -m 0644 rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits-resume.service /etc/systemd/system/restore-cpu-rapl-limits-resume.service
sudo install -D -m 0644 rapl-power-limit/usr/share/doc/system/rapl-power-limit.md /usr/share/doc/system/rapl-power-limit.md
```

Reload systemd and enable the automatic units:

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now restore-cpu-rapl-limits-monitor.service
sudo systemctl enable restore-cpu-rapl-limits-resume.service
```

The monitor service performs the initial restore itself. The one-shot
`restore-cpu-rapl-limits.service` remains available for manual or compatibility
use, but it is not required when the monitor is enabled.

Verify that the live files are regular files rather than `/home`-backed
symlinks:

```sh
ls -l /usr/local/sbin/restore-cpu-rapl-limits
ls -l /etc/systemd/system/restore-cpu-rapl-limits*.service
systemctl is-enabled restore-cpu-rapl-limits-monitor.service restore-cpu-rapl-limits-resume.service
```

## Verify

Check the MMIO long-term package limit:

```sh
cat /sys/class/powercap/intel-rapl-mmio:0/constraint_0_power_limit_uw
```

Expected value:

```text
55000000
```

Run `turbostat` under load to confirm CPU package power can rise above 25 W:

```sh
sudo turbostat --Summary --interval 1
```

Check the monitor service:

```sh
systemctl status restore-cpu-rapl-limits-monitor.service
journalctl -u restore-cpu-rapl-limits-monitor.service
```

Run a one-shot drift check:

```sh
sudo bash /usr/local/sbin/restore-cpu-rapl-limits --check
```

## Notes

The script uses 55 W for the long-term package limit because the host exposes 55 W as the maximum long-term MMIO package constraint. Short-term and peak package limits remain higher to preserve transient boost behavior.

The monitor reads the three MMIO RAPL package limit files once per second by
default and only writes when a value drifts from the expected target. This keeps
the automatic correction responsive without a continuous write loop or noisy
journal entries. Override `RAPL_POWER_LIMIT_MONITOR_INTERVAL_SECONDS` with a
systemd drop-in if a slower polling interval is preferred.
