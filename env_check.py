from __future__ import annotations

import importlib.util
import platform
import shutil
import sys


def _check_command(command: str) -> tuple[bool, str]:
    resolved = shutil.which(command)
    return (resolved is not None, resolved or "not found")


def _check_pyyaml() -> bool:
    return importlib.util.find_spec("yaml") is not None


def main() -> int:
    system = platform.system()
    release = platform.release()

    print("=" * 72)
    print("SDN REPRODUCIBILITY ENVIRONMENT CHECK")
    print("=" * 72)
    print(f"OS: {system} {release}")

    mn_ok, mn_path = _check_command("mn")
    ryu_ok, ryu_path = _check_command("ryu-manager")
    yaml_ok = _check_pyyaml()

    print("\nCommand checks:")
    print(f"  mn           : {'OK' if mn_ok else 'MISSING'} ({mn_path})")
    print(f"  ryu-manager  : {'OK' if ryu_ok else 'MISSING'} ({ryu_path})")

    print("\nPython package checks:")
    print(f"  PyYAML       : {'OK' if yaml_ok else 'MISSING'}")

    if system.lower() == "windows":
        print("\nWARNING:")
        print("  Windows host detected. Decision-grade SDN benchmarks require Linux networking semantics.")
        print("  Switch to WSL2 (Ubuntu) or a Linux VM before collecting final benchmark evidence.")

    all_ok = mn_ok and ryu_ok and yaml_ok and system.lower() != "windows"

    print("\nSummary:")
    if all_ok:
        print("  PASS: Environment is Linux-ready for reproducible SDN benchmark execution.")
        return 0

    print("  FAIL: Environment is not yet Linux-ready for decision-grade benchmark execution.")
    print("  Required baseline: Linux + Mininet + Ryu + PyYAML.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
