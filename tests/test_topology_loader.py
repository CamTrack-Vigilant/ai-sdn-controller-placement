from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import networkx as nx

from topology.canonical_topologies import load_topology_file


class TopologyLoaderTests(unittest.TestCase):
    def test_load_graphml_success_and_deterministic_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.graphml"
            graph = nx.Graph()
            graph.add_edge("b", "a", weight="2.5")
            graph.add_edge("a", "c", latency="3.0")
            nx.write_graphml(graph, path)

            loaded1 = load_topology_file(path)
            loaded2 = load_topology_file(path)

        self.assertEqual(sorted(loaded1.nodes()), ["n0", "n1", "n2"])
        self.assertEqual(sorted(loaded2.nodes()), ["n0", "n1", "n2"])
        self.assertTrue(nx.is_connected(loaded1))

        edges1 = sorted((min(u, v), max(u, v), loaded1.edges[u, v]["weight"]) for u, v in loaded1.edges())
        edges2 = sorted((min(u, v), max(u, v), loaded2.edges[u, v]["weight"]) for u, v in loaded2.edges())
        self.assertEqual(edges1, edges2)

    def test_load_gml_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.gml"
            graph = nx.Graph()
            graph.add_edge("x", "y", distance=1.7)
            nx.write_gml(graph, path)

            loaded = load_topology_file(path)

        self.assertEqual(loaded.number_of_nodes(), 2)
        self.assertEqual(loaded.number_of_edges(), 1)
        self.assertIn("weight", next(iter(loaded.edges(data=True)))[2])

    def test_unsupported_format_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.txt"
            path.write_text("not a topology", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_topology_file(path)

    def test_malformed_graphml_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "broken.graphml"
            path.write_text("<graphml><broken></graphml", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_topology_file(path)

    def test_disconnected_graph_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "disconnected.graphml"
            graph = nx.Graph()
            graph.add_edge("a", "b")
            graph.add_node("c")
            nx.write_graphml(graph, path)

            with self.assertRaises(ValueError):
                load_topology_file(path)


if __name__ == "__main__":
    unittest.main()
