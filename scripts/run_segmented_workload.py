#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import csv
import subprocess
import time
from pathlib import Path


@dataclass(frozen=True)
class SegmentResult:
    segment_index: int
    command: str
    return_code: int
    started_at_utc: str
    finished_at_utc: str
    elapsed_seconds: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a long experiment workload in thermal-friendly segments.",
    )
    parser.add_argument(
        "--command-template",
        required=True,
        help=(
            "Shell command template to execute for each segment. Supports {segment}, "
            "{segment_total}, {seed}, and {segment_label}."
        ),
    )
    parser.add_argument("--segments", type=int, default=18, help="Number of segments to run.")
    parser.add_argument(
        "--seed-start",
        type=int,
        default=42,
        help="Base seed value used to derive per-segment seeds.",
    )
    parser.add_argument(
        "--seed-stride",
        type=int,
        default=100,
        help="Increment applied to the seed for each segment.",
    )
    parser.add_argument(
        "--cooldown-seconds",
        type=int,
        default=300,
        help="Pause between segments to reduce host thermal stress.",
    )
    parser.add_argument(
        "--output-dir",
        default="results/experiment_data/segment_runs",
        help="Directory for per-segment logs and manifest.",
    )
    parser.add_argument(
        "--manifest-name",
        default="segmented_workload_manifest.csv",
        help="CSV manifest filename written inside output-dir.",
    )
    parser.add_argument(
        "--cleanup-command",
        default="sudo mn -c",
        help="Optional cleanup command run before the first segment and after each segment.",
    )
    parser.add_argument(
        "--skip-cleanup",
        action="store_true",
        help="Skip environment cleanup between segments.",
    )
    return parser.parse_args()


def _write_manifest(manifest_path: Path, results: list[SegmentResult]) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "segment_index",
                "command",
                "return_code",
                "started_at_utc",
                "finished_at_utc",
                "elapsed_seconds",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "segment_index": result.segment_index,
                    "command": result.command,
                    "return_code": result.return_code,
                    "started_at_utc": result.started_at_utc,
                    "finished_at_utc": result.finished_at_utc,
                    "elapsed_seconds": round(result.elapsed_seconds, 6),
                }
            )


def _run_shell_command(command: str, log_path: Path) -> int:
    with log_path.open("w", encoding="utf-8") as handle:
        process = subprocess.run(
            ["bash", "-lc", command],
            stdout=handle,
            stderr=subprocess.STDOUT,
            check=False,
        )
    return int(process.returncode)


def main() -> int:
    args = parse_args()
    if args.cooldown_seconds < 60:
        raise ValueError("cooldown-seconds must be at least 60 to preserve thermal comparability of tau measurements")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = output_dir / args.manifest_name
    results: list[SegmentResult] = []

    if not args.skip_cleanup:
        print("[INFO] Pre-run cleanup")
        _run_shell_command(args.cleanup_command, output_dir / "cleanup_before.log")

    total_start = time.perf_counter()
    for segment_index in range(1, args.segments + 1):
        seed = args.seed_start + ((segment_index - 1) * args.seed_stride)
        segment_label = f"segment_{segment_index:02d}_of_{args.segments:02d}"
        rendered_command = args.command_template.format(
            segment=segment_index,
            segment_total=args.segments,
            seed=seed,
            segment_label=segment_label,
        )

        print(f"[INFO] Running {segment_label}")
        started_at = datetime.now(timezone.utc).isoformat()
        segment_start = time.perf_counter()
        return_code = _run_shell_command(rendered_command, output_dir / f"{segment_label}.log")
        finished_at = datetime.now(timezone.utc).isoformat()
        elapsed_seconds = time.perf_counter() - segment_start

        results.append(
            SegmentResult(
                segment_index=segment_index,
                command=rendered_command,
                return_code=return_code,
                started_at_utc=started_at,
                finished_at_utc=finished_at,
                elapsed_seconds=elapsed_seconds,
            )
        )
        _write_manifest(manifest_path, results)

        if return_code != 0:
            print(f"[ERROR] Segment {segment_index} failed with code {return_code}")
            return return_code

        if segment_index < args.segments and args.cooldown_seconds > 0:
            print(f"[INFO] Cooling down for {args.cooldown_seconds} seconds")
            time.sleep(args.cooldown_seconds)

        if not args.skip_cleanup:
            _run_shell_command(args.cleanup_command, output_dir / f"cleanup_after_{segment_label}.log")

    total_elapsed = time.perf_counter() - total_start
    print(f"[INFO] Completed {args.segments} segments in {total_elapsed:.2f} seconds")
    print(f"[INFO] Manifest written to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())