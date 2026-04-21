from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from experiments.experiment_runner import write_manifest


class ManifestSchemaTests(unittest.TestCase):
    def test_manifest_contains_required_fields(self) -> None:
        config = {
            "topology": {"num_sites": 2},
            "experiment": {"trials": 30, "seed": 42},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            manifest_path = write_manifest(
                data_dir=data_dir,
                timestamp="20260417_020000",
                run_id="benchmark_20260417_020000",
                run_mode="decision_grade",
                config=config,
                random_seed=42,
                trials=30,
                strict_decision_grade_enabled=True,
                strict_enforcement_passed=True,
                strict_enforcement_reason="Strict decision-grade enforcement passed for trials=30.",
            )

            self.assertTrue(manifest_path.exists())
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))

        required = {
            "run_id",
            "run_mode",
            "generated_at_utc",
            "python_version",
            "system_os",
            "git_commit_hash",
            "random_seed",
            "config_hash",
            "suite_runs",
            "suite_size_target",
            "completed_30_run_suites",
            "strict_decision_grade",
            "config",
        }
        self.assertTrue(required.issubset(payload.keys()))

        self.assertEqual(payload["run_id"], "benchmark_20260417_020000")
        self.assertEqual(payload["run_mode"], "decision_grade")
        self.assertEqual(payload["suite_runs"], 30)
        self.assertEqual(payload["suite_size_target"], 30)
        self.assertEqual(payload["completed_30_run_suites"], 1)
        self.assertEqual(payload["strict_decision_grade"]["enabled"], True)
        self.assertEqual(payload["strict_decision_grade"]["passed"], True)
        self.assertTrue(isinstance(payload["config_hash"], str) and len(payload["config_hash"]) == 64)

    def test_manifest_json_is_stably_sorted(self) -> None:
        config = {"b": 2, "a": 1}

        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            manifest_path = write_manifest(
                data_dir=data_dir,
                timestamp="20260417_020001",
                run_id="benchmark_20260417_020001",
                run_mode="non_decision_grade",
                config=config,
                random_seed=7,
                trials=5,
                strict_decision_grade_enabled=False,
                strict_enforcement_passed=True,
                strict_enforcement_reason="Strict enforcement disabled (non-decision-grade mode).",
            )
            content = manifest_path.read_text(encoding="utf-8")

        # With sort_keys=True, alphabetically early keys should appear before later keys.
        self.assertLess(content.find('"config"'), content.find('"config_hash"'))
        self.assertLess(content.find('"generated_at_utc"'), content.find('"git_commit_hash"'))


if __name__ == "__main__":
    unittest.main()
