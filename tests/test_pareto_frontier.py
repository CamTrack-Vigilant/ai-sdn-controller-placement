from __future__ import annotations

import unittest

import pandas as pd

from evaluation.pareto import (
    mark_latency_reliability_pareto,
    rank_latency_reliability_compromise,
    select_best_latency_reliability_compromise,
)


class ParetoFrontierTests(unittest.TestCase):
    def test_marks_non_dominated_points(self) -> None:
        df = pd.DataFrame(
            [
                {"algorithm": "A", "average_distance": 1.0, "control_plane_reliability": 0.90},
                {"algorithm": "B", "average_distance": 2.0, "control_plane_reliability": 0.95},
                {"algorithm": "C", "average_distance": 1.5, "control_plane_reliability": 0.85},
                {"algorithm": "D", "average_distance": 1.0, "control_plane_reliability": 0.90},
            ]
        )

        marked = mark_latency_reliability_pareto(df)
        pareto_algorithms = set(marked.loc[marked["is_pareto_optimal"], "algorithm"])

        self.assertEqual(pareto_algorithms, {"A", "B", "D"})

    def test_computes_front_per_group(self) -> None:
        df = pd.DataFrame(
            [
                {
                    "scenario": "s1",
                    "algorithm": "A",
                    "average_distance": 1.0,
                    "control_plane_reliability": 0.90,
                },
                {
                    "scenario": "s1",
                    "algorithm": "B",
                    "average_distance": 2.0,
                    "control_plane_reliability": 0.95,
                },
                {
                    "scenario": "s1",
                    "algorithm": "C",
                    "average_distance": 1.2,
                    "control_plane_reliability": 0.85,
                },
                {
                    "scenario": "s2",
                    "algorithm": "X",
                    "average_distance": 3.0,
                    "control_plane_reliability": 0.60,
                },
                {
                    "scenario": "s2",
                    "algorithm": "Y",
                    "average_distance": 2.0,
                    "control_plane_reliability": 0.70,
                },
            ]
        )

        marked = mark_latency_reliability_pareto(df, group_cols=["scenario"])

        s1 = set(marked.loc[(marked["scenario"] == "s1") & marked["is_pareto_optimal"], "algorithm"])
        s2 = set(marked.loc[(marked["scenario"] == "s2") & marked["is_pareto_optimal"], "algorithm"])

        self.assertEqual(s1, {"A", "B"})
        self.assertEqual(s2, {"Y"})

    def test_compromise_ranking_prefers_closest_ideal_point(self) -> None:
        df = pd.DataFrame(
            [
                {
                    "scenario": "s1",
                    "algorithm": "A",
                    "average_distance": 1.0,
                    "control_plane_reliability": 0.70,
                },
                {
                    "scenario": "s1",
                    "algorithm": "B",
                    "average_distance": 1.2,
                    "control_plane_reliability": 0.95,
                },
                {
                    "scenario": "s1",
                    "algorithm": "C",
                    "average_distance": 1.4,
                    "control_plane_reliability": 0.85,
                },
            ]
        )

        ranked = rank_latency_reliability_compromise(df, group_cols=["scenario"])
        best = ranked.loc[ranked["compromise_rank"] == 1, "algorithm"].iloc[0]

        # Point B is closest to ideal due to high reliability with low latency penalty.
        self.assertEqual(best, "B")

    def test_select_best_compromise_returns_one_per_group(self) -> None:
        df = pd.DataFrame(
            [
                {
                    "scenario": "s1",
                    "algorithm": "A",
                    "average_distance": 1.0,
                    "control_plane_reliability": 0.80,
                },
                {
                    "scenario": "s1",
                    "algorithm": "B",
                    "average_distance": 1.2,
                    "control_plane_reliability": 0.95,
                },
                {
                    "scenario": "s1",
                    "algorithm": "C",
                    "average_distance": 1.5,
                    "control_plane_reliability": 0.70,
                },
                {
                    "scenario": "s2",
                    "algorithm": "X",
                    "average_distance": 2.5,
                    "control_plane_reliability": 0.60,
                },
                {
                    "scenario": "s2",
                    "algorithm": "Y",
                    "average_distance": 2.1,
                    "control_plane_reliability": 0.70,
                },
            ]
        )

        best = select_best_latency_reliability_compromise(df, group_cols=["scenario"])
        by_scenario = dict(zip(best["scenario"], best["algorithm"]))

        self.assertEqual(set(by_scenario.keys()), {"s1", "s2"})
        self.assertEqual(by_scenario["s1"], "B")
        self.assertEqual(by_scenario["s2"], "Y")


if __name__ == "__main__":
    unittest.main()
