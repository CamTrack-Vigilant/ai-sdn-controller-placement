import React, { useState, useEffect, useMemo } from 'react';
import {
  TopologyFamily,
  AlgorithmType,
  NetworkGraph,
  AlgorithmResult,
} from './types';
import {
  generateInternet2Topology,
  generateAttMplsTopology,
  generateBarabasiAlbertTopology,
  generateWaxmanTopology,
  generateMultiSiteMeshTopology,
  runRandomPlacement,
  runGreedyKCenterPlacement,
  runKMeansPlacement,
  runGeneticAlgorithmPlacement,
  runBanditRlPlacement,
  calculateParetoFrontier,
  rankIdealPointCompromise,
  evaluatePlacement,
} from './lib/graphAlgorithms';
import { TopologyView } from './components/TopologyView';
import { AlgorithmScorecard } from './components/AlgorithmScorecard';
import { ParetoChart } from './components/ParetoChart';
import { FactorialMatrixTable } from './components/FactorialMatrixTable';
import { HypothesisDashboard } from './components/HypothesisDashboard';
import {
  Activity,
  Sliders,
  Play,
  RotateCcw,
  Network,
  Cpu,
  Layers,
  Award,
  BookOpen,
  Zap,
  BarChart2,
  FileCode2,
} from 'lucide-react';

export const App: React.FC = () => {
  // Navigation
  const [activeTab, setActiveTab] = useState<'lab' | 'pareto' | 'matrix' | 'research'>('lab');

  // Topology parameters
  const [selectedTopologyFamily, setSelectedTopologyFamily] = useState<TopologyFamily>('internet2');
  const [nodeScale, setNodeScale] = useState<number>(20);
  const [seed, setSeed] = useState<number>(42);

  // Controller placement parameters
  const [controllerBudget, setControllerBudget] = useState<number>(3);
  const [activeAlgorithm, setActiveAlgorithm] = useState<AlgorithmType>('greedy_k_center');

  // AI Algorithm Hyperparameters
  const [gaGenerations, setGaGenerations] = useState<number>(40);
  const [gaPopulation, setGaPopulation] = useState<number>(30);
  const [rlEpisodes, setRlEpisodes] = useState<number>(150);
  const [rlLatencyWeight, setRlLatencyWeight] = useState<number>(1.0);
  const [rlReliabilityWeight, setRlReliabilityWeight] = useState<number>(0.3);

  // Fault simulation state
  const [failedEdges, setFailedEdges] = useState<Set<string>>(new Set());
  const [failedControllers, setFailedControllers] = useState<Set<string>>(new Set());

  // Cached benchmark results for current topology and k
  const [resultsMap, setResultsMap] = useState<Map<AlgorithmType, AlgorithmResult>>(new Map());
  const [isRunningAll, setIsRunningAll] = useState<boolean>(false);

  // 1. Generate or load topology
  const graph: NetworkGraph = useMemo(() => {
    switch (selectedTopologyFamily) {
      case 'internet2':
        return generateInternet2Topology(seed);
      case 'att_mpls':
        return generateAttMplsTopology(seed);
      case 'barabasi_albert':
        return generateBarabasiAlbertTopology(nodeScale, 3, seed);
      case 'waxman':
        return generateWaxmanTopology(nodeScale, 0.4, 0.25, seed);
      case 'multi_site_mesh':
        return generateMultiSiteMeshTopology(4, Math.max(4, Math.floor(nodeScale / 4)), seed);
      default:
        return generateInternet2Topology(seed);
    }
  }, [selectedTopologyFamily, nodeScale, seed]);

  // Ensure controller budget doesn't exceed node count
  const effectiveBudget = Math.min(controllerBudget, graph.nodes.length);

  // 2. Solve algorithms when parameters change
  const computeAlgorithm = (algo: AlgorithmType, currentGraph: NetworkGraph): AlgorithmResult => {
    switch (algo) {
      case 'random':
        return runRandomPlacement(currentGraph, effectiveBudget, seed);
      case 'greedy_k_center':
        return runGreedyKCenterPlacement(currentGraph, effectiveBudget);
      case 'kmeans':
        return runKMeansPlacement(currentGraph, effectiveBudget, seed);
      case 'genetic':
        return runGeneticAlgorithmPlacement(currentGraph, effectiveBudget, {
          generations: gaGenerations,
          populationSize: gaPopulation,
          seed,
        });
      case 'bandit_rl':
        return runBanditRlPlacement(currentGraph, effectiveBudget, {
          episodes: rlEpisodes,
          latencyWeight: rlLatencyWeight,
          reliabilityWeight: rlReliabilityWeight,
          seed,
        });
    }
  };

  // Run all algorithms to have a complete multi-objective comparison set
  const runAllSolvers = () => {
    setIsRunningAll(true);
    setTimeout(() => {
      const algos: AlgorithmType[] = ['random', 'greedy_k_center', 'kmeans', 'genetic', 'bandit_rl'];
      const newMap = new Map<AlgorithmType, AlgorithmResult>();

      for (const a of algos) {
        newMap.set(a, computeAlgorithm(a, graph));
      }

      // Pareto and compromise ranking
      const allResults = Array.from(newMap.values());
      const paretoSet = calculateParetoFrontier(allResults);
      const ranked = rankIdealPointCompromise(paretoSet);

      const finalMap = new Map<AlgorithmType, AlgorithmResult>();
      for (const r of ranked) {
        finalMap.set(r.algorithm, r);
      }

      setResultsMap(finalMap);
      setIsRunningAll(false);
    }, 50);
  };

  // Re-run when topology or budget changes
  useEffect(() => {
    runAllSolvers();
    setFailedEdges(new Set());
    setFailedControllers(new Set());
  }, [selectedTopologyFamily, nodeScale, controllerBudget, seed]);

  // Current active result
  const activeResult = resultsMap.get(activeAlgorithm) || computeAlgorithm(activeAlgorithm, graph);
  const baselineResult = resultsMap.get('random');

  // Handle active graph with fault injection
  const evaluatedActiveResult: AlgorithmResult = useMemo(() => {
    if (failedEdges.size === 0 && failedControllers.size === 0) {
      return activeResult;
    }

    // Apply active faults to metrics dynamically
    const survivingControllers = activeResult.controllers.filter(c => !failedControllers.has(c));
    const activeEdges = graph.edges.map(e => ({
      ...e,
      isFailed: failedEdges.has(e.id),
    }));

    const faultedGraph: NetworkGraph = {
      ...graph,
      edges: activeEdges,
    };

    const metrics = evaluatePlacement(
      faultedGraph,
      survivingControllers,
      undefined,
      activeResult.metrics.runtimeMs,
      activeResult.metrics.iterationsToConverge,
      activeResult.metrics.iterationsBudget
    );

    return {
      ...activeResult,
      metrics,
    };
  }, [activeResult, failedEdges, failedControllers, graph]);

  // Toggle link failure
  const handleToggleEdge = (edgeId: string) => {
    setFailedEdges(prev => {
      const next = new Set(prev);
      if (next.has(edgeId)) {
        next.delete(edgeId);
      } else {
        next.add(edgeId);
      }
      return next;
    });
  };

  // Toggle controller failure
  const handleToggleController = (nodeId: string) => {
    setFailedControllers(prev => {
      const next = new Set(prev);
      if (next.has(nodeId)) {
        next.delete(nodeId);
      } else {
        next.add(nodeId);
      }
      return next;
    });
  };

  const handleResetFailures = () => {
    setFailedEdges(new Set());
    setFailedControllers(new Set());
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Global Navigation Bar */}
      <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-tr from-cyan-600 to-blue-600 rounded-lg shadow-lg shadow-cyan-900/40">
              <Network className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-bold text-slate-100 text-base tracking-tight">
                  ai-sdn-controller-placement
                </h1>
                <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                  Decision-Grade
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Multi-Objective Benchmarking of AI & Heuristic Controller Placement
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
            <button
              onClick={() => setActiveTab('lab')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-colors ${
                activeTab === 'lab'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              <span>Interactive Lab</span>
            </button>

            <button
              onClick={() => setActiveTab('pareto')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-colors ${
                activeTab === 'pareto'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Award className="w-3.5 h-3.5" />
              <span>Pareto Frontier</span>
            </button>

            <button
              onClick={() => setActiveTab('matrix')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-colors ${
                activeTab === 'matrix'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BarChart2 className="w-3.5 h-3.5" />
              <span>Factorial Matrix</span>
            </button>

            <button
              onClick={() => setActiveTab('research')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-colors ${
                activeTab === 'research'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Research Hub</span>
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* TAB 1: INTERACTIVE BENCHMARK LAB */}
        {activeTab === 'lab' && (
          <div className="space-y-6">
            {/* Top Control Grid */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                {/* 1. Topology Selection */}
                <div>
                  <label className="block text-slate-400 font-semibold mb-1.5">
                    1. Network Topology
                  </label>
                  <select
                    value={selectedTopologyFamily}
                    onChange={(e) => setSelectedTopologyFamily(e.target.value as TopologyFamily)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 font-medium focus:outline-none focus:border-cyan-500"
                  >
                    <option value="internet2">Internet2 Backbone (11 Nodes)</option>
                    <option value="att_mpls">AT&T MPLS Backbone (21 Nodes)</option>
                    <option value="barabasi_albert">Barabási-Albert (Scale-Free)</option>
                    <option value="waxman">Waxman (Geographic Random)</option>
                    <option value="multi_site_mesh">Multi-Site Ring & Mesh (4 Sites)</option>
                  </select>
                  <span className="text-[11px] text-slate-400 mt-1 block">
                    {selectedTopologyFamily === 'internet2' || selectedTopologyFamily === 'att_mpls'
                      ? 'Heller et al. (2012) canonical reference'
                      : 'Synthetic factorial testbed model'}
                  </span>
                </div>

                {/* 2. Scale (Nodes) */}
                <div>
                  <label className="block text-slate-400 font-semibold mb-1.5">
                    2. Scale (Total Nodes: {graph.nodes.length})
                  </label>
                  {selectedTopologyFamily === 'barabasi_albert' ||
                  selectedTopologyFamily === 'waxman' ||
                  selectedTopologyFamily === 'multi_site_mesh' ? (
                    <div className="flex items-center gap-2">
                      {[20, 50, 100].map((count) => (
                        <button
                          key={count}
                          onClick={() => setNodeScale(count)}
                          className={`flex-1 py-2 rounded-lg font-bold border transition-colors ${
                            nodeScale === count
                              ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50'
                              : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700'
                          }`}
                        >
                          N={count}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <div className="bg-slate-950 border border-slate-800/80 rounded-lg py-2 px-3 text-slate-400">
                      Fixed by canonical architecture
                    </div>
                  )}
                  <span className="text-[11px] text-slate-400 mt-1 block">
                    {graph.edges.length} total links ({graph.siteCount} sites/regions)
                  </span>
                </div>

                {/* 3. Controller Budget k */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-slate-400 font-semibold">
                      3. Controller Budget (k):
                    </label>
                    <span className="font-mono font-bold text-cyan-400 text-sm">
                      k = {effectiveBudget}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max={Math.min(8, graph.nodes.length)}
                    value={effectiveBudget}
                    onChange={(e) => setControllerBudget(parseInt(e.target.value, 10))}
                    className="w-full accent-cyan-500 bg-slate-950 cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-mono">
                    <span>k=1</span>
                    <span>k=3</span>
                    <span>k=5</span>
                    <span>k={Math.min(8, graph.nodes.length)}</span>
                  </div>
                </div>

                {/* 4. Placement Algorithm Selector */}
                <div>
                  <label className="block text-slate-400 font-semibold mb-1.5">
                    4. Placement Algorithm
                  </label>
                  <select
                    value={activeAlgorithm}
                    onChange={(e) => setActiveAlgorithm(e.target.value as AlgorithmType)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 font-medium focus:outline-none focus:border-cyan-500"
                  >
                    <option value="greedy_k_center">Greedy k-Center (Heller / Gonzalez)</option>
                    <option value="genetic">Genetic Algorithm (GA Multi-Gen)</option>
                    <option value="bandit_rl">Adaptive Bandit RL / AP-DQN</option>
                    <option value="kmeans">k-Means Geometric Clustering</option>
                    <option value="random">Random Placement (Baseline)</option>
                  </select>
                  <div className="flex items-center justify-between mt-1.5">
                    <button
                      onClick={runAllSolvers}
                      disabled={isRunningAll}
                      className="text-[11px] text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1"
                    >
                      <RotateCcw className={`w-3 h-3 ${isRunningAll ? 'animate-spin' : ''}`} />
                      Re-solve Matrix (Seed: {seed})
                    </button>
                    <button
                      onClick={() => setSeed((s) => s + 100)}
                      className="text-[11px] text-slate-400 hover:text-slate-300"
                    >
                      Change Seed
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Live Metrics Scorecard */}
            <AlgorithmScorecard
              result={evaluatedActiveResult}
              baselineResult={baselineResult}
            />

            {/* Interactive Topology Graph Visualizer */}
            <TopologyView
              graph={graph}
              activeControllers={evaluatedActiveResult.controllers}
              failedEdges={failedEdges}
              failedControllers={failedControllers}
              onToggleEdgeFailure={handleToggleEdge}
              onToggleControllerFailure={handleToggleController}
              onResetFailures={handleResetFailures}
            />

            {/* Algorithm Quick Switcher Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              {(['greedy_k_center', 'genetic', 'bandit_rl', 'kmeans', 'random'] as AlgorithmType[]).map((algoKey) => {
                const res = resultsMap.get(algoKey);
                const isSelected = activeAlgorithm === algoKey;

                return (
                  <div
                    key={algoKey}
                    onClick={() => setActiveAlgorithm(algoKey)}
                    className={`p-3 rounded-xl border cursor-pointer transition-all ${
                      isSelected
                        ? 'bg-slate-900 border-cyan-500 shadow-lg shadow-cyan-950/50'
                        : 'bg-slate-900/60 border-slate-800/80 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className="font-semibold text-slate-200">
                        {algoKey === 'greedy_k_center'
                          ? 'Greedy k-Center'
                          : algoKey === 'genetic'
                          ? 'Genetic (GA)'
                          : algoKey === 'bandit_rl'
                          ? 'Bandit RL'
                          : algoKey === 'kmeans'
                          ? 'k-Means'
                          : 'Random'}
                      </span>
                      {res?.isParetoOptimal && (
                        <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400" title="Pareto Optimal" />
                      )}
                    </div>
                    <div className="text-sm font-bold text-slate-100 font-mono">
                      {res ? `${res.metrics.averageDistance} ms` : '-'}
                    </div>
                    <div className="text-[10px] text-slate-400 mt-1 flex justify-between">
                      <span>{res ? (res.metrics.runtimeMs < 1 ? '<1 ms' : `${res.metrics.runtimeMs}ms`) : '-'}</span>
                      <span>Rel: {res ? `${(res.metrics.controlPlaneReliability * 100).toFixed(0)}%` : '-'}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* TAB 2: PARETO TRADE-OFF FRONTIER */}
        {activeTab === 'pareto' && (
          <div className="space-y-6">
            <ParetoChart
              results={Array.from(resultsMap.values())}
              selectedAlgorithmId={activeAlgorithm}
              onSelectAlgorithm={(algo) => {
                setActiveAlgorithm(algo.algorithm);
                setActiveTab('lab');
              }}
            />

            {/* Algorithm Comparison Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
              <h3 className="font-bold text-slate-100 text-base mb-3 flex items-center gap-2">
                <Sliders className="w-4 h-4 text-cyan-400" />
                Scenario Multi-Objective Comparative Matrix
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="py-2.5 px-3">Algorithm</th>
                      <th className="py-2.5 px-3">Avg Latency (ms)</th>
                      <th className="py-2.5 px-3">Worst Latency (ms)</th>
                      <th className="py-2.5 px-3">N-1 Link Reliability</th>
                      <th className="py-2.5 px-3">Load Imbalance (Std)</th>
                      <th className="py-2.5 px-3">Runtime</th>
                      <th className="py-2.5 px-3">Ideal Distance</th>
                      <th className="py-2.5 px-3">Compromise Rank</th>
                      <th className="py-2.5 px-3 text-center">Pareto</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-mono">
                    {Array.from(resultsMap.values()).map((r) => (
                      <tr key={r.algorithm} className="hover:bg-slate-800/40">
                        <td className="py-2.5 px-3 font-sans font-semibold text-slate-100">
                          {r.algorithmName}
                        </td>
                        <td className="py-2.5 px-3 text-cyan-300 font-bold">
                          {r.metrics.averageDistance} ms
                        </td>
                        <td className="py-2.5 px-3 text-amber-300">
                          {r.metrics.worstCaseDistance} ms
                        </td>
                        <td className="py-2.5 px-3 text-emerald-300">
                          {(r.metrics.controlPlaneReliability * 100).toFixed(1)}%
                        </td>
                        <td className="py-2.5 px-3 text-slate-400">
                          {r.metrics.controllerLoadStd}
                        </td>
                        <td className="py-2.5 px-3 text-slate-400">
                          {r.metrics.runtimeMs < 1 ? '< 1 ms' : `${r.metrics.runtimeMs} ms`}
                        </td>
                        <td className="py-2.5 px-3 text-slate-300">
                          {r.idealPointDistance ?? '-'}
                        </td>
                        <td className="py-2.5 px-3 font-sans">
                          {r.compromiseRank ? (
                            <span className="px-2 py-0.5 rounded text-[11px] bg-slate-800 font-bold text-slate-200">
                              Rank #{r.compromiseRank}
                            </span>
                          ) : (
                            '-'
                          )}
                        </td>
                        <td className="py-2.5 px-3 text-center">
                          {r.isParetoOptimal ? (
                            <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold">
                              OPTIMAL
                            </span>
                          ) : (
                            <span className="text-slate-600">Dominated</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: FULL FACTORIAL BENCHMARK MATRIX */}
        {activeTab === 'matrix' && <FactorialMatrixTable />}

        {/* TAB 4: RESEARCH METHODOLOGY & HYPOTHESES */}
        {activeTab === 'research' && <HypothesisDashboard />}
      </main>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800/80 py-4 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks</span>
          <span className="font-mono text-slate-400">
            Methodology Section 8.4.1 Parity &middot; IEEE Standard References &middot; Deterministic Seeding
          </span>
        </div>
      </footer>
    </div>
  );
};
