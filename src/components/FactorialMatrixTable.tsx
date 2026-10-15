import React, { useState } from 'react';
import { FACTORIAL_SUMMARY_DATA } from '../data/benchmarkDatasets';
import { FactorialBenchmarkRow } from '../types';
import { Filter, Download, ArrowUpDown, Award, CheckCircle2 } from 'lucide-react';

export const FactorialMatrixTable: React.FC = () => {
  const [modelFilter, setModelFilter] = useState<string>('all');
  const [nodesFilter, setNodesFilter] = useState<string>('all');
  const [budgetFilter, setBudgetFilter] = useState<string>('all');
  const [sortField, setSortField] = useState<keyof FactorialBenchmarkRow>('avgLatencyMean');
  const [sortAsc, setSortAsc] = useState<boolean>(true);

  // Filtered dataset
  const filtered = FACTORIAL_SUMMARY_DATA.filter((row) => {
    if (modelFilter !== 'all' && row.topologyModel !== modelFilter) return false;
    if (nodesFilter !== 'all' && row.nodeCount.toString() !== nodesFilter) return false;
    if (budgetFilter !== 'all' && row.controllerBudget.toString() !== budgetFilter) return false;
    return true;
  });

  // Sorted
  const sorted = [...filtered].sort((a, b) => {
    const valA = a[sortField];
    const valB = b[sortField];
    if (typeof valA === 'number' && typeof valB === 'number') {
      return sortAsc ? valA - valB : valB - valA;
    }
    return 0;
  });

  const handleSort = (field: keyof FactorialBenchmarkRow) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  // Export CSV
  const handleExportCSV = () => {
    const headers = [
      'topology_model',
      'node_count',
      'controller_budget',
      'algorithm',
      'avg_latency_mean',
      'avg_latency_std',
      'runtime_ms_mean',
      'runtime_ms_std',
      'iterations_to_converge_mean',
      'latency_gain_vs_random_pct',
      'efficiency_score',
      'efficiency_rank',
      'is_pareto_optimal',
    ];

    const rows = sorted.map((r) => [
      r.topologyModel,
      r.nodeCount,
      r.controllerBudget,
      r.algorithm,
      r.avgLatencyMean,
      r.avgLatencyStd,
      r.runtimeMsMean,
      r.runtimeMsStd,
      r.iterationsToConvergeMean,
      r.latencyGainVsRandomPct,
      r.efficiencyScore,
      r.efficiencyRank,
      r.isParetoOptimal,
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `factorial_latency_cost_export.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex flex-col">
      {/* Header & Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-4 border-b border-slate-800">
        <div>
          <h3 className="font-bold text-slate-100 text-base flex items-center gap-2">
            Factorial Latency-Cost Benchmark Matrix
            <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              60 Scenario Trials
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Empirical results across Barabási-Albert & Waxman models, N ∈ &#123;20, 50, 100&#125;, k ∈ &#123;3, 5&#125;
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-600 hover:bg-cyan-500 text-white transition-colors shadow"
        >
          <Download className="w-3.5 h-3.5" />
          Export SPSS/CSV
        </button>
      </div>

      {/* Filters Bar */}
      <div className="flex flex-wrap items-center gap-3 mb-4 bg-slate-950/70 p-3 rounded-lg border border-slate-800/80 text-xs">
        <div className="flex items-center gap-1.5 text-slate-400">
          <Filter className="w-3.5 h-3.5 text-cyan-400" />
          <span className="font-medium">Filter by:</span>
        </div>

        {/* Model Filter */}
        <div className="flex items-center gap-1">
          <label className="text-slate-400">Topology:</label>
          <select
            value={modelFilter}
            onChange={(e) => setModelFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            <option value="all">All Topologies</option>
            <option value="barabasi_albert">Barabási-Albert</option>
            <option value="waxman">Waxman Geographic</option>
          </select>
        </div>

        {/* Nodes Filter */}
        <div className="flex items-center gap-1">
          <label className="text-slate-400">Scale (Nodes):</label>
          <select
            value={nodesFilter}
            onChange={(e) => setNodesFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            <option value="all">All Scales</option>
            <option value="20">20 Nodes</option>
            <option value="50">50 Nodes</option>
            <option value="100">100 Nodes</option>
          </select>
        </div>

        {/* Budget Filter */}
        <div className="flex items-center gap-1">
          <label className="text-slate-400">Controllers (k):</label>
          <select
            value={budgetFilter}
            onChange={(e) => setBudgetFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            <option value="all">All Budgets</option>
            <option value="3">k = 3 Controllers</option>
            <option value="5">k = 5 Controllers</option>
          </select>
        </div>

        <span className="ml-auto text-slate-400">
          Showing <strong>{sorted.length}</strong> of {FACTORIAL_SUMMARY_DATA.length} runs
        </span>
      </div>

      {/* Responsive Data Table */}
      <div className="overflow-x-auto rounded-lg border border-slate-800">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950 text-slate-400 font-semibold uppercase tracking-wider border-b border-slate-800 text-[11px]">
            <tr>
              <th className="py-2.5 px-3">Topology</th>
              <th className="py-2.5 px-2">Nodes</th>
              <th className="py-2.5 px-2">k</th>
              <th className="py-2.5 px-3">Algorithm</th>
              <th
                onClick={() => handleSort('avgLatencyMean')}
                className="py-2.5 px-3 cursor-pointer hover:text-cyan-400 transition-colors"
              >
                <div className="flex items-center gap-1">
                  Avg Latency (ms)
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('runtimeMsMean')}
                className="py-2.5 px-3 cursor-pointer hover:text-cyan-400 transition-colors"
              >
                <div className="flex items-center gap-1">
                  Runtime (ms)
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('iterationsToConvergeMean')}
                className="py-2.5 px-3 cursor-pointer hover:text-cyan-400 transition-colors"
              >
                <div className="flex items-center gap-1">
                  Conv. Iters
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('latencyGainVsRandomPct')}
                className="py-2.5 px-3 cursor-pointer hover:text-cyan-400 transition-colors"
              >
                <div className="flex items-center gap-1">
                  Gain vs Random
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('efficiencyRank')}
                className="py-2.5 px-2 cursor-pointer hover:text-cyan-400 transition-colors"
              >
                <div className="flex items-center gap-1">
                  Eff. Rank
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th className="py-2.5 px-3 text-center">Pareto</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono">
            {sorted.map((row, idx) => (
              <tr
                key={idx}
                className="hover:bg-slate-800/40 transition-colors"
              >
                <td className="py-2 px-3 font-sans capitalize text-slate-200">
                  {row.topologyModel.replace('_', ' ')}
                </td>
                <td className="py-2 px-2 text-slate-400">{row.nodeCount}</td>
                <td className="py-2 px-2 text-cyan-300 font-bold">{row.controllerBudget}</td>
                <td className="py-2 px-3 font-sans font-medium text-slate-100">
                  <span
                    className={`inline-block w-2 h-2 rounded-full mr-2 ${
                      row.algorithm === 'genetic'
                        ? 'bg-purple-400'
                        : row.algorithm === 'bandit_rl'
                        ? 'bg-amber-400'
                        : row.algorithm === 'greedy_k_center'
                        ? 'bg-blue-400'
                        : row.algorithm === 'kmeans'
                        ? 'bg-emerald-400'
                        : 'bg-slate-500'
                    }`}
                  />
                  {row.algorithm === 'greedy_k_center'
                    ? 'Greedy k-Center'
                    : row.algorithm === 'bandit_rl'
                    ? 'Bandit RL'
                    : row.algorithm === 'genetic'
                    ? 'Genetic Algorithm'
                    : row.algorithm === 'kmeans'
                    ? 'k-Means'
                    : 'Random'}
                </td>
                <td className="py-2 px-3 text-slate-100 font-semibold">
                  {row.avgLatencyMean.toFixed(2)}
                  {row.avgLatencyStd > 0 && (
                    <span className="text-[10px] text-slate-500 ml-1">
                      ±{row.avgLatencyStd.toFixed(2)}
                    </span>
                  )}
                </td>
                <td className="py-2 px-3 text-slate-300">
                  {row.runtimeMsMean < 1 ? '< 0.5' : row.runtimeMsMean.toFixed(1)}
                </td>
                <td className="py-2 px-3 text-slate-400">
                  {row.iterationsToConvergeMean.toFixed(1)}
                </td>
                <td
                  className={`py-2 px-3 font-semibold ${
                    row.latencyGainVsRandomPct > 0 ? 'text-emerald-400' : 'text-slate-500'
                  }`}
                >
                  {row.latencyGainVsRandomPct > 0
                    ? `+${row.latencyGainVsRandomPct.toFixed(1)}%`
                    : '0.0%'}
                </td>
                <td className="py-2 px-2 text-center">
                  <span
                    className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-[10px] font-bold ${
                      row.efficiencyRank === 1
                        ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                        : row.efficiencyRank === 2
                        ? 'bg-blue-500/20 text-blue-300 border border-blue-500/40'
                        : 'text-slate-500'
                    }`}
                  >
                    #{row.efficiencyRank}
                  </span>
                </td>
                <td className="py-2 px-3 text-center">
                  {row.isParetoOptimal ? (
                    <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold">
                      <CheckCircle2 className="w-3 h-3" /> YES
                    </span>
                  ) : (
                    <span className="text-slate-600 text-[11px]">-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
