from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
import unittest

from experiments.experiment_runner import DEFAULT_CONFIG, _deep_merge, resolve_config


class ExperimentConfigTests(unittest.TestCase):
    def _make_args(self, **overrides: object) -> argparse.Namespace:
        base = {
            "config": None,
            "sites": None,
            "nodes_per_site": None,
            "controllers": None,
            "trials": None,
            "seed": None,
            "metrics": None,
            "log_level": "INFO",
            "log_file": None,
        }
        base.update(overrides)
        return argparse.Namespace(**base)

    def test_deep_merge_preserves_nested_defaults(self) -> None:
        base = {
            "topology": {"num_sites": 4, "nodes_per_site": 12},
            "outputs": {"logs_dir": "logs", "graph_dir": "results/graphs"},
        }
        updates = {
            "topology": {"nodes_per_site": 8},
            "outputs": {"logs_dir": "custom_logs"},
            "extra": {"enabled": True},
        }

        merged = _deep_merge(base, updates)

        self.assertEqual(merged["topology"]["num_sites"], 4)
        self.assertEqual(merged["topology"]["nodes_per_site"], 8)
        self.assertEqual(merged["outputs"]["graph_dir"], "results/graphs")
        self.assertEqual(merged["outputs"]["logs_dir"], "custom_logs")
        self.assertEqual(merged["extra"], {"enabled": True})

        # Ensure input dictionaries are not mutated.
        self.assertEqual(base["topology"]["nodes_per_site"], 12)
        self.assertEqual(base["outputs"]["logs_dir"], "logs")

    def test_resolve_config_with_file_and_cli_overrides(self) -> None:
        file_config = {
            "topology": {"nodes_per_site": 10, "inter_site_links": 3},
            "experiment": {"num_controllers": 2, "trials": 7},
            "outputs": {"logs_dir": "custom_logs"},
            "rl_logging": {"enabled": False},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "experiment_config.json"
            config_path.write_text(json.dumps(file_config), encoding="utf-8")

            args = self._make_args(
                config=str(config_path),
                sites=5,
                controllers=4,
                trials=9,
                seed=99,
                metrics="average_distance,resilience_ratio",
            )

            resolved = resolve_config(args)

        self.assertEqual(resolved["topology"]["num_sites"], 5)
        self.assertEqual(resolved["topology"]["nodes_per_site"], 10)
        self.assertEqual(resolved["topology"]["inter_site_links"], 3)
        self.assertEqual(resolved["topology"]["seed"], 99)

        self.assertEqual(resolved["experiment"]["num_controllers"], 4)
        self.assertEqual(resolved["experiment"]["trials"], 9)
        self.assertEqual(resolved["experiment"]["seed"], 99)
        self.assertEqual(
            resolved["experiment"]["metrics_to_plot"],
            ["average_distance", "resilience_ratio"],
        )

        self.assertEqual(resolved["outputs"]["logs_dir"], "custom_logs")
        self.assertFalse(resolved["rl_logging"]["enabled"])

        self.assertEqual(
            resolved["rl_objective"]["latency_weight"],
            DEFAULT_CONFIG["rl_objective"]["latency_weight"],
        )
        self.assertEqual(
            resolved["rl_objective"]["reliability_weight"],
            DEFAULT_CONFIG["rl_objective"]["reliability_weight"],
        )

        # Keep one default field assertion to verify deep default fallback still works.
        self.assertEqual(resolved["outputs"]["graph_dir"], DEFAULT_CONFIG["outputs"]["graph_dir"])


if __name__ == "__main__":
    unittest.main()
