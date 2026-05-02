# RAPL Power Limit

`rapl-power-limit` is a root-target GNU Stow package for the ThinkPad P16 Gen 2. It restores the CPU package MMIO RAPL limits at boot and after resume.

The package exists because this host has been observed entering a platform state where CPU package power is held around 25 W even though temperatures are low and normal performance settings are active. The immediate cause is a low MMIO-backed RAPL long-term package limit.

## Files

- `rapl-power-limit/usr/local/sbin/restore-cpu-rapl-limits`
- `rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits.service`
- `rapl-power-limit/etc/systemd/system/restore-cpu-rapl-limits-resume.service`
- `rapl-power-limit/usr/share/doc/system/rapl-power-limit.md`

This package targets `/`, not `$HOME`, because it installs machine-level files under `/etc`, `/usr/local`, and `/usr/share`.

## Install

Dry run from the repository root:

```sh
sudo stow -n -v --target=/ rapl-power-limit
```

Install and enable:

```sh
sudo stow --target=/ rapl-power-limit
sudo systemctl daemon-reload
sudo systemctl enable --now restore-cpu-rapl-limits.service
sudo systemctl enable restore-cpu-rapl-limits-resume.service
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

## Notes

The script uses 55 W for the long-term package limit because the host exposes 55 W as the maximum long-term MMIO package constraint. Short-term and peak package limits remain higher to preserve transient boost behavior.
