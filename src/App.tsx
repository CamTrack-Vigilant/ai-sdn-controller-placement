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
  generateUnizuluMultiCampusTopology,
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
import { UnizuluCrestSvg } from './components/UnizuluLogo';
import { UnizuluHeroBanner } from './components/UnizuluOfficialWave';
import { UnizuluSlideDeck } from './components/UnizuluSlideDeck';
import { RotateCcw, Download } from 'lucide-react';

export const App: React.FC = () => {
  // Primary View Navigation
  const [activeTab, setActiveTab] = useState<
    'lab' | 'pareto' | 'matrix' | 'research' | 'slides'
  >('lab');

  // Topology & Experimental Factors
  const [selectedTopologyFamily, setSelectedTopologyFamily] =
    useState<TopologyFamily>('internet2');
  const [nodeScale, setNodeScale] = useState<number>(20);
  const [seed, setSeed] = useState<number>(42);

  // Controller Placement Parameters
  const [controllerBudget, setControllerBudget] = useState<number>(3);
  const [activeAlgorithm, setActiveAlgorithm] =
    useState<AlgorithmType>('greedy_k_center');

  // AI Hyperparameters (Farahi et al. 2026 & GA calibration)
  const [gaGenerations, setGaGenerations] = useState<number>(40);
  const [gaPopulation] = useState<number>(30);
  const [rlEpisodes, setRlEpisodes] = useState<number>(150);
  const [rlLatencyWeight] = useState<number>(1.0);
  const [rlReliabilityWeight] = useState<number>(0.25);

  // Interactive Fault Injection State
  const [failedEdges, setFailedEdges] = useState<Set<string>>(new Set());
  const [failedControllers, setFailedControllers] = useState<Set<string>>(new Set());

  // Evaluated Benchmark Results Map
  const [resultsMap, setResultsMap] = useState<Map<AlgorithmType, AlgorithmResult>>(
    new Map()
  );
  const [isRunningAll, setIsRunningAll] = useState<boolean>(false);

  // 1. Construct Active Network Graph
  const graph: NetworkGraph = useMemo(() => {
    switch (selectedTopologyFamily) {
      case 'internet2':
        return generateInternet2Topology(seed);
      case 'unizulu_wan':
        return generateUnizuluMultiCampusTopology(seed);
      case 'att_mpls':
        return generateAttMplsTopology(seed);
      case 'barabasi_albert':
        return generateBarabasiAlbertTopology(nodeScale, 3, seed);
      case 'waxman':
        return generateWaxmanTopology(nodeScale, 0.4, 0.25, seed);
      case 'multi_site_mesh':
        return generateMultiSiteMeshTopology(
          4,
          Math.max(4, Math.floor(nodeScale / 4)),
          seed
        );
      default:
        return generateInternet2Topology(seed);
    }
  }, [selectedTopologyFamily, nodeScale, seed]);

  const effectiveBudget = Math.min(controllerBudget, graph.nodes.length);

  // 2. Execute Single Placement Solver
  const computeAlgorithm = (
    algo: AlgorithmType,
    currentGraph: NetworkGraph
  ): AlgorithmResult => {
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

  // 3. Execute Full 5-Algorithm Comparative Suite
  const runAllSolvers = () => {
    setIsRunningAll(true);
    setTimeout(() => {
      const algos: AlgorithmType[] = [
        'random',
        'greedy_k_center',
        'kmeans',
        'genetic',
        'bandit_rl',
      ];
      const newMap = new Map<AlgorithmType, AlgorithmResult>();

      for (const a of algos) {
        newMap.set(a, computeAlgorithm(a, graph));
      }

      const allResults = Array.from(newMap.values());
      const paretoSet = calculateParetoFrontier(allResults);
      const ranked = rankIdealPointCompromise(paretoSet);

      const finalMap = new Map<AlgorithmType, AlgorithmResult>();
      for (const r of ranked) {
        finalMap.set(r.algorithm, r);
      }

      setResultsMap(finalMap);
      setIsRunningAll(false);
    }, 30);
  };

  useEffect(() => {
    runAllSolvers();
    setFailedEdges(new Set());
    setFailedControllers(new Set());
  }, [selectedTopologyFamily, nodeScale, controllerBudget, seed, gaGenerations, rlEpisodes]);

  const activeResult =
    resultsMap.get(activeAlgorithm) || computeAlgorithm(activeAlgorithm, graph);
  const baselineResult = resultsMap.get('random');

  // Re-evaluate metrics live under injected link/controller failures
  const evaluatedActiveResult: AlgorithmResult = useMemo(() => {
    if (failedEdges.size === 0 && failedControllers.size === 0) {
      return activeResult;
    }

    const survivingControllers = activeResult.controllers.filter(
      (c) => !failedControllers.has(c)
    );
    const activeEdges = graph.edges.map((e) => ({
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

  const handleToggleEdge = (edgeId: string) => {
    setFailedEdges((prev) => {
      const next = new Set(prev);
      if (next.has(edgeId)) next.delete(edgeId);
      else next.add(edgeId);
      return next;
    });
  };

  const handleToggleController = (nodeId: string) => {
    setFailedControllers((prev) => {
      const next = new Set(prev);
      if (next.has(nodeId)) next.delete(nodeId);
      else next.add(nodeId);
      return next;
    });
  };

  const handleResetFailures = () => {
    setFailedEdges(new Set());
    setFailedControllers(new Set());
  };

  // Export Current Scenario Comparison CSV
  const handleExportCurrentScenario = () => {
    const headers = [
      'institution',
      'candidate',
      'student_number',
      'topology',
      'nodes',
      'controllers_k',
      'seed',
      'algorithm',
      'avg_latency_ms',
      'worst_latency_ms',
      'n1_link_reliability_pct',
      'controller_failover_ratio',
      'load_std',
      'runtime_ms',
      'pareto_optimal',
      'compromise_rank',
    ];

    const rows = Array.from(resultsMap.values()).map((r) => [
      'University of Zululand',
      'Thabang Nhlokoma Buthelezi',
      '230011908',
      graph.family,
      graph.nodes.length,
      effectiveBudget,
      seed,
      r.algorithm,
      r.metrics.averageDistance,
      r.metrics.worstCaseDistance,
      (r.metrics.controlPlaneReliability * 100).toFixed(2),
      r.metrics.resilienceRatio,
      r.metrics.controllerLoadStd,
      r.metrics.runtimeMs,
      r.isParetoOptimal ? 'TRUE' : 'FALSE',
      r.compromiseRank ?? '',
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute(
      'download',
      `UNIZULU_${graph.family}_k${effectiveBudget}_seed${seed}.csv`
    );
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const tabTitleMap: Record<typeof activeTab, string> = {
    lab: 'Interactive Multi-Site SDN Simulation Lab',
    pareto: 'Non-Dominated Pareto Frontier & Compromise Analysis',
    matrix: 'Full Factorial Latency-Cost Matrix (60 Scenario Cells)',
    research: 'Honours Research Proposal & Deductive Hypotheses',
    slides: 'Proposal Stage Plan for R and D (Official UNIZULU Slide Deck)',
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-[#0F172A] flex flex-col">
      {/* Top Bar Contract: 3 Zones separated by gap-8 (Brand | 5 Nav Links | 1 Primary Action) */}
      <header className="sticky top-0 z-50 bg-white border-b border-slate-200 border-t-4 border-t-[#0057A8]">
        <div className="max-w-[1380px] mx-auto px-6 h-16 flex items-center justify-between gap-8">
          {/* Zone 1: Single-line Brand Wordmark */}
          <a
            href="#top"
            onClick={(e) => {
              e.preventDefault();
              setActiveTab('lab');
            }}
            className="flex items-center gap-2.5 text-base font-bold tracking-tight text-[#0057A8] whitespace-nowrap shrink-0"
          >
            <UnizuluCrestSvg className="w-8 h-9 shrink-0" />
            <span>University of Zululand</span>
          </a>

          {/* Zone 2: 5 Single-line Navigation Links */}
          <nav
            aria-label="Primary Workspace Navigation"
            className="flex items-center gap-6 text-sm font-medium text-slate-600 overflow-x-auto"
          >
            <button
              onClick={() => setActiveTab('lab')}
              className={`py-5 border-b-2 transition-colors whitespace-nowrap shrink-0 ${
                activeTab === 'lab'
                  ? 'border-[#0057A8] text-[#0057A8] font-semibold'
                  : 'border-transparent hover:text-slate-900'
              }`}
            >
              Simulation Lab
            </button>
            <button
              onClick={() => setActiveTab('pareto')}
              className={`py-5 border-b-2 transition-colors whitespace-nowrap shrink-0 ${
                activeTab === 'pareto'
                  ? 'border-[#0057A8] text-[#0057A8] font-semibold'
                  : 'border-transparent hover:text-slate-900'
              }`}
            >
              Pareto Frontier
            </button>
            <button
              onClick={() => setActiveTab('matrix')}
              className={`py-5 border-b-2 transition-colors whitespace-nowrap shrink-0 ${
                activeTab === 'matrix'
                  ? 'border-[#0057A8] text-[#0057A8] font-semibold'
                  : 'border-transparent hover:text-slate-900'
              }`}
            >
              Factorial Matrix
            </button>
            <button
              onClick={() => setActiveTab('research')}
              className={`py-5 border-b-2 transition-colors whitespace-nowrap shrink-0 ${
                activeTab === 'research'
                  ? 'border-[#0057A8] text-[#0057A8] font-semibold'
                  : 'border-transparent hover:text-slate-900'
              }`}
            >
              Research Proposal
            </button>
            <button
              onClick={() => setActiveTab('slides')}
              className={`py-5 border-b-2 transition-colors whitespace-nowrap shrink-0 ${
                activeTab === 'slides'
                  ? 'border-[#84383E] text-[#84383E] font-semibold'
                  : 'border-transparent hover:text-slate-900'
              }`}
            >
              Presentation Deck
            </button>
          </nav>

          {/* Zone 3: 1 Primary Action Button */}
          <div className="flex items-center shrink-0">
            <button
              onClick={handleExportCurrentScenario}
              className="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-[#0057A8] hover:bg-[#004488] rounded-md transition-colors whitespace-nowrap shrink-0"
            >
              <Download className="w-3.5 h-3.5" />
              Export Scenario CSV
            </button>
          </div>
        </div>
      </header>

      {/* Official University of Zululand Wave Banner (from attached school design) */}
      <UnizuluHeroBanner
        activeTabLabel={tabTitleMap[activeTab]}
        onOpenSlideDeck={
          activeTab !== 'slides' ? () => setActiveTab('slides') : undefined
        }
      />

      {/* Main Workspace Container */}
      <main className="flex-1 max-w-[1380px] w-full mx-auto px-6 py-8">
        {/* TAB 1: SIMULATION LAB */}
        {activeTab === 'lab' && (
          <div className="space-y-6">
            {/* Parameter Calibration & Experimental Controls */}
            <section
              aria-label="Experimental Scenario Calibration"
              className="bg-white border border-slate-200 border-t-2 border-t-[#0057A8] rounded-lg p-5"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 text-xs">
                {/* 1. Network Topology */}
                <div>
                  <label
                    htmlFor="select-topology"
                    className="block text-slate-700 font-semibold mb-1.5"
                  >
                    01. Experimental Network Topology
                  </label>
                  <select
                    id="select-topology"
                    value={selectedTopologyFamily}
                    onChange={(e) =>
                      setSelectedTopologyFamily(e.target.value as TopologyFamily)
                    }
                    className="w-full bg-[#F8FAFC] border border-slate-300 rounded-md px-3 py-2 text-slate-900 font-medium focus:outline-none focus:border-[#0057A8]"
                  >
                    <option value="internet2">
                      Internet2 Canonical Backbone (11 Nodes)
                    </option>
                    <option value="att_mpls">
                      AT&amp;T MPLS Canonical Backbone (21 Nodes)
                    </option>
                    <option value="unizulu_wan">
                      UNIZULU Multi-Campus &amp; SANReN KZN (12 Nodes)
                    </option>
                    <option value="barabasi_albert">
                      Barabási-Albert Scale-Free (Preferential)
                    </option>
                    <option value="waxman">
                      Waxman Geographic Random Backbone
                    </option>
                    <option value="multi_site_mesh">
                      Multi-Site Ring &amp; Mesh (4 Sites)
                    </option>
                  </select>
                  <div className="text-[11px] text-slate-500 mt-1.5">
                    {selectedTopologyFamily === 'internet2' ||
                    selectedTopologyFamily === 'att_mpls'
                      ? 'Heller et al. (2012) baseline parity testbed'
                      : selectedTopologyFamily === 'unizulu_wan'
                      ? 'KwaDlangezwa · Richards Bay · SANReN KZN ring'
                      : 'Section 8.3 synthetic factorial model'}
                  </div>
                </div>

                {/* 2. Scale (Nodes) */}
                <div>
                  <label className="block text-slate-700 font-semibold mb-1.5">
                    02. Topology Scale (N = {graph.nodes.length} Switches)
                  </label>
                  {selectedTopologyFamily === 'barabasi_albert' ||
                  selectedTopologyFamily === 'waxman' ||
                  selectedTopologyFamily === 'multi_site_mesh' ? (
                    <div className="flex items-center gap-1.5">
                      {[20, 50, 100].map((count) => (
                        <button
                          key={count}
                          onClick={() => setNodeScale(count)}
                          className={`flex-1 py-2 rounded-md font-mono font-semibold border transition-colors whitespace-nowrap shrink-0 ${
                            nodeScale === count
                              ? 'bg-[#0057A8] text-white border-[#0057A8]'
                              : 'bg-[#F8FAFC] text-slate-700 border-slate-300 hover:border-[#0057A8]'
                          }`}
                        >
                          N={count}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <div className="bg-[#F8FAFC] border border-slate-200 rounded-md py-2 px-3 text-slate-600 font-mono">
                      Fixed Reference: {graph.nodes.length} Nodes · {graph.edges.length} Links
                    </div>
                  )}
                  <div className="text-[11px] text-slate-500 mt-1.5 font-mono tabular-nums">
                    {graph.edges.length} optical links across {graph.siteCount} regional sites
                  </div>
                </div>

                {/* 3. Controller Budget k */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label
                      htmlFor="slider-budget"
                      className="text-slate-700 font-semibold"
                    >
                      03. Controller Budget (k)
                    </label>
                    <span className="font-mono font-bold text-[#0057A8] text-sm tabular-nums">
                      k = {effectiveBudget}
                    </span>
                  </div>
                  <input
                    id="slider-budget"
                    type="range"
                    min="1"
                    max={Math.min(8, graph.nodes.length)}
                    value={effectiveBudget}
                    onChange={(e) => setControllerBudget(parseInt(e.target.value, 10))}
                    className="w-full accent-[#0057A8] cursor-pointer"
                  />
                  <div className="flex justify-between text-[11px] text-slate-500 mt-1 font-mono tabular-nums">
                    <span>k=1</span>
                    <span>k=3</span>
                    <span>k=5</span>
                    <span>k={Math.min(8, graph.nodes.length)}</span>
                  </div>
                </div>

                {/* 4. Placement Algorithm & Seed Control */}
                <div>
                  <label
                    htmlFor="select-algorithm"
                    className="block text-slate-700 font-semibold mb-1.5"
                  >
                    04. Placement Optimization Method
                  </label>
                  <select
                    id="select-algorithm"
                    value={activeAlgorithm}
                    onChange={(e) =>
                      setActiveAlgorithm(e.target.value as AlgorithmType)
                    }
                    className="w-full bg-[#F8FAFC] border border-slate-300 rounded-md px-3 py-2 text-slate-900 font-medium focus:outline-none focus:border-[#0057A8]"
                  >
                    <option value="greedy_k_center">
                      Greedy k-Center (Heller / Gonzalez)
                    </option>
                    <option value="genetic">
                      Genetic Algorithm (Meta-Heuristic)
                    </option>
                    <option value="bandit_rl">
                      AP-DQN / Bandit RL (Farahi et al., 2026)
                    </option>
                    <option value="kmeans">
                      k-Means Coordinate Clustering
                    </option>
                    <option value="random">
                      Random Placement (Stochastic Floor)
                    </option>
                  </select>
                  <div className="flex items-center justify-between mt-1.5">
                    <button
                      onClick={runAllSolvers}
                      disabled={isRunningAll}
                      className="text-[11px] text-[#0057A8] hover:text-[#004488] font-semibold flex items-center gap-1 whitespace-nowrap"
                    >
                      <RotateCcw
                        className={`w-3 h-3 ${isRunningAll ? 'animate-spin' : ''}`}
                      />
                      Re-compute Trial (Seed {seed})
                    </button>
                    <div className="flex items-center gap-1 font-mono text-[11px]">
                      {[42, 142, 242].map((sVal) => (
                        <button
                          key={sVal}
                          onClick={() => setSeed(sVal)}
                          className={`px-1.5 py-0.5 rounded transition-colors ${
                            seed === sVal
                              ? 'bg-[#84383E] text-white font-semibold'
                              : 'text-slate-600 hover:bg-slate-100'
                          }`}
                        >
                          {sVal}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Secondary AI Calibration Row (GA Generations & RL Episodes) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-4 pt-4 border-t border-slate-100 text-xs">
                <div className="flex items-center justify-between gap-4">
                  <label htmlFor="ga-generations" className="text-slate-600 font-medium">
                    Genetic Algorithm Budget:{' '}
                    <strong className="font-mono text-slate-900">
                      {gaGenerations} gen
                    </strong>
                  </label>
                  <input
                    id="ga-generations"
                    type="range"
                    min="20"
                    max="100"
                    step="10"
                    value={gaGenerations}
                    onChange={(e) => setGaGenerations(parseInt(e.target.value, 10))}
                    className="w-36 accent-[#84383E] cursor-pointer"
                  />
                </div>

                <div className="flex items-center justify-between gap-4">
                  <label htmlFor="rl-episodes" className="text-slate-600 font-medium">
                    AP-DQN / RL Training Budget:{' '}
                    <strong className="font-mono text-slate-900">{rlEpisodes} ep</strong>
                  </label>
                  <input
                    id="rl-episodes"
                    type="range"
                    min="50"
                    max="300"
                    step="25"
                    value={rlEpisodes}
                    onChange={(e) => setRlEpisodes(parseInt(e.target.value, 10))}
                    className="w-36 accent-[#84383E] cursor-pointer"
                  />
                </div>

                <div className="flex items-center justify-end text-slate-500 font-mono text-[11px] tabular-nums">
                  Composite Reward: R = -(1.0 · Latency) + (0.25 · Reliability)
                </div>
              </div>
            </section>

            {/* Multi-Objective Telemetry Scorecard */}
            <AlgorithmScorecard
              result={evaluatedActiveResult}
              baselineResult={baselineResult}
              activeFaultCount={failedEdges.size + failedControllers.size}
            />

            {/* Interactive Network Topology & Fault Injection Canvas */}
            <TopologyView
              graph={graph}
              activeControllers={evaluatedActiveResult.controllers}
              failedEdges={failedEdges}
              failedControllers={failedControllers}
              onToggleEdgeFailure={handleToggleEdge}
              onToggleControllerFailure={handleToggleController}
              onResetFailures={handleResetFailures}
            />

            {/* Side-by-Side 5-Method Scenario Comparison Selector */}
            <section
              aria-label="Five-Algorithm Comparative Selector"
              className="bg-white border border-slate-200 rounded-lg p-5"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 pb-3 mb-4 border-b border-slate-200">
                <h3 className="text-sm font-bold text-slate-900">
                  Cross-Algorithm Comparison on {graph.name} (k = {effectiveBudget}, Seed ={' '}
                  {seed})
                </h3>
                <span className="text-xs text-slate-500">
                  Click any algorithm row or card to inspect its controller placement on the topology canvas
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                {(
                  [
                    'greedy_k_center',
                    'genetic',
                    'bandit_rl',
                    'kmeans',
                    'random',
                  ] as AlgorithmType[]
                ).map((algoKey) => {
                  const res = resultsMap.get(algoKey);
                  const isSelected = activeAlgorithm === algoKey;

                  return (
                    <button
                      key={algoKey}
                      onClick={() => setActiveAlgorithm(algoKey)}
                      className={`p-3.5 rounded-md border text-left transition-colors ${
                        isSelected
                          ? 'bg-[#EBF4FC] border-[#0057A8]'
                          : 'bg-[#FAFBFD] border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <div className="flex items-center justify-between text-xs mb-1.5">
                        <span className="font-bold text-slate-900 truncate">
                          {algoKey === 'greedy_k_center'
                            ? 'Greedy k-Center'
                            : algoKey === 'genetic'
                            ? 'Genetic (GA)'
                            : algoKey === 'bandit_rl'
                            ? 'AP-DQN / RL'
                            : algoKey === 'kmeans'
                            ? 'k-Means'
                            : 'Random'}
                        </span>
                        {res?.isParetoOptimal && (
                          <span className="text-[10px] font-mono font-semibold text-[#0057A8] whitespace-nowrap">
                            ● Pareto
                          </span>
                        )}
                      </div>

                      <div className="flex items-baseline gap-1 font-mono tabular-nums">
                        <span className="text-lg font-bold text-slate-900">
                          {res ? res.metrics.averageDistance.toFixed(2) : '-'}
                        </span>
                        <span className="text-[11px] text-slate-500">ms</span>
                      </div>

                      <div className="text-[11px] text-slate-600 font-mono tabular-nums mt-2 pt-2 border-t border-slate-200/80 flex justify-between">
                        <span>
                          {res
                            ? res.metrics.runtimeMs < 1
                              ? '<1.0 ms'
                              : `${res.metrics.runtimeMs.toFixed(1)} ms`
                            : '-'}
                        </span>
                        <span className="text-[#84383E] font-medium">
                          Rel:{' '}
                          {res
                            ? `${(res.metrics.controlPlaneReliability * 100).toFixed(1)}%`
                            : '-'}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </section>
          </div>
        )}

        {/* TAB 2: PARETO FRONTIER */}
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

            {/* Scenario Multi-Objective Comparative Ledger */}
            <div className="bg-white border border-slate-200 rounded-lg p-6">
              <div className="pb-4 mb-4 border-b border-slate-200">
                <div className="text-xs text-[#84383E] font-semibold mb-1">
                  Active Scenario: {graph.name} · k = {effectiveBudget} · Seed = {seed}
                </div>
                <h3 className="font-bold text-slate-900 text-base">
                  Multi-Objective Performance &amp; Compromise Ranking Table
                </h3>
              </div>

              <div className="overflow-x-auto border border-slate-200 rounded-md">
                <table className="w-full text-left text-xs text-slate-800">
                  <thead className="bg-[#F8FAFC] text-slate-600 font-semibold border-b border-slate-200">
                    <tr>
                      <th className="py-3 px-3.5">Algorithm</th>
                      <th className="py-3 px-3.5">Mean Latency (ms)</th>
                      <th className="py-3 px-3.5">Worst Latency (ms)</th>
                      <th className="py-3 px-3.5">N-1 Link Reliability</th>
                      <th className="py-3 px-3.5">Load Imbalance (σ)</th>
                      <th className="py-3 px-3.5">Runtime Cost</th>
                      <th className="py-3 px-3.5">Ideal Point Dist.</th>
                      <th className="py-3 px-3.5">Compromise Rank</th>
                      <th className="py-3 px-3.5">Pareto State</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 font-mono tabular-nums">
                    {Array.from(resultsMap.values()).map((r) => (
                      <tr
                        key={r.algorithm}
                        onClick={() => {
                          setActiveAlgorithm(r.algorithm);
                          setActiveTab('lab');
                        }}
                        className="hover:bg-slate-50 cursor-pointer transition-colors"
                      >
                        <td className="py-2.5 px-3.5 font-sans font-semibold text-slate-900">
                          {r.algorithmName}
                        </td>
                        <td className="py-2.5 px-3.5 text-[#0057A8] font-semibold">
                          {r.metrics.averageDistance.toFixed(2)} ms
                        </td>
                        <td className="py-2.5 px-3.5 text-slate-700">
                          {r.metrics.worstCaseDistance.toFixed(2)} ms
                        </td>
                        <td className="py-2.5 px-3.5 text-emerald-700 font-semibold">
                          {(r.metrics.controlPlaneReliability * 100).toFixed(2)}%
                        </td>
                        <td className="py-2.5 px-3.5 text-slate-600">
                          {r.metrics.controllerLoadStd.toFixed(2)}
                        </td>
                        <td className="py-2.5 px-3.5 text-slate-700">
                          {r.metrics.runtimeMs < 1
                            ? '< 1.0 ms'
                            : `${r.metrics.runtimeMs.toFixed(2)} ms`}
                        </td>
                        <td className="py-2.5 px-3.5 text-slate-700">
                          {r.idealPointDistance !== undefined
                            ? r.idealPointDistance.toFixed(3)
                            : '-'}
                        </td>
                        <td className="py-2.5 px-3.5 font-semibold text-[#84383E]">
                          {r.compromiseRank ? `#${r.compromiseRank}` : '-'}
                        </td>
                        <td className="py-2.5 px-3.5 font-sans">
                          {r.isParetoOptimal ? (
                            <span className="text-[#0057A8] font-semibold">● Optimal</span>
                          ) : (
                            <span className="text-slate-500">○ Dominated</span>
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

        {/* TAB 3: FACTORIAL BENCHMARK MATRIX */}
        {activeTab === 'matrix' && <FactorialMatrixTable />}

        {/* TAB 4: UNIVERSITY OF ZULULAND RESEARCH PROPOSAL & HYPOTHESES */}
        {activeTab === 'research' && <HypothesisDashboard />}

        {/* TAB 5: OFFICIAL UNIZULU PROPOSAL STAGE PLAN FOR R&D SLIDE DECK */}
        {activeTab === 'slides' && (
          <UnizuluSlideDeck
            graph={graph}
            results={Array.from(resultsMap.values())}
            effectiveBudget={effectiveBudget}
            seed={seed}
          />
        )}
      </main>

      {/* Quiet Institutional Footer with UNIZULU Burgundy & Blue Trim */}
      <footer className="bg-white border-t border-slate-200 border-b-4 border-b-[#84383E] py-5 text-xs text-slate-600">
        <div className="max-w-[1380px] mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-bold text-[#0057A8]">University of Zululand</span>
            <span aria-hidden="true">·</span>
            <span>Department of Computer Science</span>
            <span aria-hidden="true">·</span>
            <span>Thabang Nhlokoma Buthelezi (230011908)</span>
          </div>
          <div className="flex flex-wrap items-center gap-2 text-slate-500">
            <span>Supervised by Prof. P. Mudali &amp; Dr. S. Zwane</span>
            <span aria-hidden="true">·</span>
            <span className="italic text-[#84383E] font-medium">
              A Node for African Thought · Diligentia Cresco
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
};
