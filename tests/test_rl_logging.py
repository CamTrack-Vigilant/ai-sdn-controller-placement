from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import networkx as nx

from algorithms.ai.reinforcement_learning import bandit_rl_controller_placement


class ReinforcementLearningLoggingTests(unittest.TestCase):
    def test_bandit_rl_writes_jsonl_trace(self) -> None:
        graph = nx.path_graph([f"n{i}" for i in range(6)])

        latency_weight = 1.5
        reliability_weight = 0.75

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "logs" / "rl_training.jsonl"

            placement = bandit_rl_controller_placement(
                graph=graph,
                num_controllers=2,
                episodes=10,
                epsilon=0.2,
                candidate_pool_size=16,
                seed=7,
                log_path=str(log_path),
                log_every=3,
                run_label="unit_test",
                latency_weight=latency_weight,
                reliability_weight=reliability_weight,
            )

            self.assertEqual(len(placement), 2)
            self.assertEqual(len(set(placement)), 2)
            self.assertTrue(log_path.exists())

            records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

        self.assertGreaterEqual(len(records), 3)
        self.assertEqual(records[0]["event"], "run_start")
        self.assertEqual(records[-1]["event"], "run_end")

        run_ids = {record["run_id"] for record in records}
        self.assertEqual(len(run_ids), 1)

        episode_records = [record for record in records if record["event"] == "episode"]
        self.assertEqual([record["episode"] for record in episode_records], [1, 3, 6, 9, 10])

        self.assertIn("num_actions", records[0])
        self.assertIn("epsilon_start", records[0])
        self.assertEqual(records[0]["latency_weight"], latency_weight)
        self.assertEqual(records[0]["reliability_weight"], reliability_weight)

        # Reward should match the configured composite objective formula.
        first_episode = episode_records[0]
        expected_reward = (
            -(latency_weight * float(first_episode["selected_action_avg_distance"]))
            + (reliability_weight * float(first_episode["selected_action_reliability"]))
        )
        self.assertAlmostEqual(float(first_episode["reward"]), expected_reward, places=10)

        self.assertIn("best_action", records[-1])
        self.assertIn("top_actions", records[-1])
        self.assertTrue(records[-1]["top_actions"])

    def test_log_every_must_be_positive(self) -> None:
        graph = nx.path_graph(["a", "b", "c"])

        with self.assertRaises(ValueError):
            bandit_rl_controller_placement(
                graph=graph,
                num_controllers=1,
                episodes=5,
                log_path="unused.jsonl",
                log_every=0,
            )

    def test_negative_weights_are_rejected(self) -> None:
        graph = nx.path_graph(["a", "b", "c"])

        with self.assertRaises(ValueError):
            bandit_rl_controller_placement(
                graph=graph,
                num_controllers=1,
                latency_weight=-1.0,
            )

        with self.assertRaises(ValueError):
            bandit_rl_controller_placement(
                graph=graph,
                num_controllers=1,
                reliability_weight=-0.1,
            )


if __name__ == "__main__":
    unittest.main()
