from __future__ import annotations

from dataclasses import dataclass
import os
import threading
import time
from typing import Optional

import psutil


@dataclass(frozen=True)
class ResourceSnapshot:
    cpu_percent: float
    rss_memory_mb: float
    io_read_bytes: int
    io_write_bytes: int
    samples: int
    process_found: bool
    status: str
    thread_cpu_percent: float | None = None


class ResourceMonitor:
    """
    Sample process-level telemetry and optional thread CPU utilization.

    The monitor is designed for two targets:
    - algorithm execution context (current Python process + current thread)
    - Ryu controller process (ryu-manager)
    """

    def __init__(
        self,
        process: psutil.Process | None,
        *,
        sample_interval_s: float = 0.1,
        thread_native_id: int | None = None,
        process_found: bool = True,
        status: str = "ok",
    ) -> None:
        self._process = process
        self._sample_interval_s = sample_interval_s
        self._thread_native_id = thread_native_id
        self._process_found = process_found
        self._status = status

        self._cpu_samples: list[float] = []
        self._rss_samples_mb: list[float] = []
        self._thread_cpu_samples: list[float] = []

        self._first_io: tuple[int, int] | None = None
        self._last_io: tuple[int, int] | None = None

        self._prev_thread_cpu_time: float | None = None
        self._prev_thread_sample_ts: float | None = None

        self._stop_event = threading.Event()
        self._worker: threading.Thread | None = None

    @classmethod
    def for_algorithm(
        cls,
        *,
        sample_interval_s: float = 0.1,
        thread_native_id: int | None = None,
    ) -> "ResourceMonitor":
        try:
            process = psutil.Process(os.getpid())
        except Exception:
            return cls.unavailable(status="algorithm_monitor_init_failed")
        native_id = thread_native_id if thread_native_id is not None else threading.get_native_id()
        return cls(
            process,
            sample_interval_s=sample_interval_s,
            thread_native_id=native_id,
            process_found=True,
            status="ok",
        )

    @classmethod
    def for_ryu(cls, *, sample_interval_s: float = 0.1) -> "ResourceMonitor":
        process = _find_ryu_process()
        return cls(
            process,
            sample_interval_s=sample_interval_s,
            thread_native_id=None,
            process_found=process is not None,
            status="ok" if process is not None else "process_not_found",
        )

    @classmethod
    def unavailable(cls, *, status: str) -> "ResourceMonitor":
        return cls(
            process=None,
            sample_interval_s=0.1,
            thread_native_id=None,
            process_found=False,
            status=status,
        )

    def start(self) -> None:
        if self._process is None:
            return

        try:
            # Prime CPU sampling so subsequent reads reflect interval deltas.
            self._process.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            self._process = None
            self._process_found = False
            self._status = "process_unavailable"
            return

        self._stop_event.clear()
        self._worker = threading.Thread(target=self._sample_loop, daemon=True)
        self._worker.start()

    def stop(self) -> ResourceSnapshot:
        self._stop_event.set()
        if self._worker is not None:
            self._worker.join(timeout=max(1.0, self._sample_interval_s * 4))

        cpu_percent = float(sum(self._cpu_samples) / len(self._cpu_samples)) if self._cpu_samples else 0.0
        rss_memory_mb = max(self._rss_samples_mb) if self._rss_samples_mb else 0.0

        io_read_bytes = 0
        io_write_bytes = 0
        if self._first_io is not None and self._last_io is not None:
            io_read_bytes = max(0, self._last_io[0] - self._first_io[0])
            io_write_bytes = max(0, self._last_io[1] - self._first_io[1])

        thread_cpu_percent = None
        if self._thread_cpu_samples:
            thread_cpu_percent = float(sum(self._thread_cpu_samples) / len(self._thread_cpu_samples))

        return ResourceSnapshot(
            cpu_percent=cpu_percent,
            rss_memory_mb=rss_memory_mb,
            io_read_bytes=io_read_bytes,
            io_write_bytes=io_write_bytes,
            samples=len(self._cpu_samples),
            process_found=self._process_found,
            status=self._status,
            thread_cpu_percent=thread_cpu_percent,
        )

    def _sample_loop(self) -> None:
        while not self._stop_event.is_set():
            self._take_sample()
            self._stop_event.wait(self._sample_interval_s)

    def _take_sample(self) -> None:
        process = self._process
        if process is None:
            return

        try:
            cpu = process.cpu_percent(None)
            mem = process.memory_info()
            io = process.io_counters()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            self._process = None
            self._process_found = False
            self._status = "process_unavailable"
            return

        self._cpu_samples.append(float(cpu))
        self._rss_samples_mb.append(float(mem.rss) / (1024.0 * 1024.0))

        current_io = (int(io.read_bytes), int(io.write_bytes))
        if self._first_io is None:
            self._first_io = current_io
        self._last_io = current_io

        if self._thread_native_id is not None:
            self._sample_thread_cpu(process)

    def _sample_thread_cpu(self, process: psutil.Process) -> None:
        now = time.perf_counter()
        try:
            thread_times = process.threads()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return

        target = next((thread for thread in thread_times if thread.id == self._thread_native_id), None)
        if target is None:
            return

        cpu_time = float(target.user_time + target.system_time)
        if self._prev_thread_cpu_time is None or self._prev_thread_sample_ts is None:
            self._prev_thread_cpu_time = cpu_time
            self._prev_thread_sample_ts = now
            return

        wall_delta = now - self._prev_thread_sample_ts
        cpu_delta = cpu_time - self._prev_thread_cpu_time

        self._prev_thread_cpu_time = cpu_time
        self._prev_thread_sample_ts = now

        if wall_delta <= 0:
            return

        thread_cpu_percent = max(0.0, min(100.0, (cpu_delta / wall_delta) * 100.0))
        self._thread_cpu_samples.append(thread_cpu_percent)


def _find_ryu_process() -> Optional[psutil.Process]:
    for process in psutil.process_iter(["name", "cmdline"]):
        try:
            name = (process.info.get("name") or "").lower()
            cmdline = " ".join(process.info.get("cmdline") or []).lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

        if "ryu-manager" in name or "ryu-manager" in cmdline:
            return process

    return None
