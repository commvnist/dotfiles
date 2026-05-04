# RAPL MMIO Power Limit Restore

This package restores the CPU package MMIO RAPL limits used on the ThinkPad P16 Gen 2 when firmware or resume state leaves the long-term package limit at 25 W.

The observed failure mode is that the MSR-backed package limit remains high while the MMIO-backed package limit is reset to a low value. In that state, `turbostat` reports low CPU temperature and no thermal throttle flag, but package power remains pinned near 25 W. Reapplying the MMIO package limits restores normal performance. The monitor service handles later platform rewrites by checking the sysfs values and restoring only when they drift.

## Installed files

These files are boot-critical and must be installed as real files on the root
filesystem. Do not leave the live systemd unit files or executable as symlinks
into `/home`; systemd can load enabled units before `/home` is mounted, which
makes those units look missing during boot.

```text
/usr/local/sbin/restore-cpu-rapl-limits
/etc/systemd/system/restore-cpu-rapl-limits.service
/etc/systemd/system/restore-cpu-rapl-limits-monitor.service
/etc/systemd/system/restore-cpu-rapl-limits-resume.service
/usr/share/doc/system/rapl-power-limit.md
```

The installed script writes these package limits:

```text
long-term package limit: 55 W
short-term package limit: 157 W
peak package limit: 234 W
```

The long-term value is 55 W because this host exposes 55 W as the maximum for the long-term MMIO package constraint. Short-term and peak limits remain higher so transient boost still works.

## Install

Run install commands from the repository root:

```sh
cd /home/naek/system
```

If this package was previously stowed into `/`, disable the old generated unit
links and remove the stowed symlinks first:

```sh
sudo systemctl disable --now restore-cpu-rapl-limits-monitor.service
sudo systemctl disable restore-cpu-rapl-limits.service restore-cpu-rapl-limits-resume.service
sudo stow --delete --target=/ rapl-power-limit
```

Copy the repository files onto the root filesystem as real files:

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

The monitor unit restores the limits at start, then reads the MMIO RAPL package
limit files once per second and writes the expected values back only after
detected drift. The resume unit still runs after wake so resume-related resets
are corrected immediately.

The one-shot `restore-cpu-rapl-limits.service` remains available for manual or
compatibility use. It is not required when the monitor is enabled.

Verify the live files are not symlinks into the repository:

```sh
ls -l /usr/local/sbin/restore-cpu-rapl-limits
ls -l /etc/systemd/system/restore-cpu-rapl-limits*.service
```

## Manual run

```sh
sudo bash /usr/local/sbin/restore-cpu-rapl-limits
```

Run a one-shot drift check without writing:

```sh
sudo bash /usr/local/sbin/restore-cpu-rapl-limits --check
```

Verify the MMIO long-term package limit:

```sh
cat /sys/class/powercap/intel-rapl-mmio:0/constraint_0_power_limit_uw
```

Expected value:

```text
55000000
```

Use `turbostat` under load to confirm package power can rise above 25 W:

```sh
sudo turbostat --Summary --interval 1
```

Check automatic corrections:

```sh
systemctl status restore-cpu-rapl-limits-monitor.service
journalctl -u restore-cpu-rapl-limits-monitor.service
```
