from __future__ import annotations

import time
import unittest

from evaluation.telemetry import ResourceMonitor


class TelemetryTests(unittest.TestCase):
    def test_algorithm_monitor_collects_snapshot(self) -> None:
        monitor = ResourceMonitor.for_algorithm(sample_interval_s=0.02)
        monitor.start()

        # Small CPU activity to guarantee monitor samples while running.
        _ = sum(i * i for i in range(20000))
        time.sleep(0.08)

        snapshot = monitor.stop()

        self.assertTrue(snapshot.process_found)
        self.assertEqual(snapshot.status, "ok")
        self.assertGreaterEqual(snapshot.samples, 1)
        self.assertGreaterEqual(snapshot.cpu_percent, 0.0)
        self.assertGreaterEqual(snapshot.rss_memory_mb, 0.0)
        self.assertGreaterEqual(snapshot.io_read_bytes, 0)
        self.assertGreaterEqual(snapshot.io_write_bytes, 0)

    def test_unavailable_monitor_returns_safe_snapshot(self) -> None:
        monitor = ResourceMonitor.unavailable(status="process_not_found")
        monitor.start()
        snapshot = monitor.stop()

        self.assertFalse(snapshot.process_found)
        self.assertEqual(snapshot.status, "process_not_found")
        self.assertEqual(snapshot.samples, 0)
        self.assertEqual(snapshot.cpu_percent, 0.0)
        self.assertEqual(snapshot.rss_memory_mb, 0.0)
        self.assertEqual(snapshot.io_read_bytes, 0)
        self.assertEqual(snapshot.io_write_bytes, 0)


if __name__ == "__main__":
    unittest.main()
