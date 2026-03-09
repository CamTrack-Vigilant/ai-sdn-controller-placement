from __future__ import annotations

import unittest

import networkx as nx

from evaluation.metrics import control_plane_reliability_single_link_failure


class ControlPlaneReliabilityTests(unittest.TestCase):
    def test_triangle_stays_fully_reachable(self) -> None:
        graph = nx.cycle_graph(["a", "b", "c"])
        reliability = control_plane_reliability_single_link_failure(graph, ["a"])
        self.assertAlmostEqual(reliability, 1.0, places=7)

    def test_path_graph_drops_reachability(self) -> None:
        graph = nx.path_graph(["n0", "n1", "n2"])
        reliability = control_plane_reliability_single_link_failure(graph, ["n1"])
        # Any single edge loss isolates one endpoint -> 2/3 nodes remain reachable.
        self.assertAlmostEqual(reliability, 2.0 / 3.0, places=7)

    def test_empty_controller_set_is_zero_reliability(self) -> None:
        graph = nx.path_graph(["x", "y", "z"])
        reliability = control_plane_reliability_single_link_failure(graph, [])
        self.assertEqual(reliability, 0.0)


if __name__ == "__main__":
    unittest.main()
