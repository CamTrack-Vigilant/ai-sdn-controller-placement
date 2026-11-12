import React, { useState } from 'react';
import { FACTORIAL_SUMMARY_DATA } from '../data/benchmarkDatasets';
import { FactorialBenchmarkRow } from '../types';
import { Download, ArrowUpDown } from 'lucide-react';

export const FactorialMatrixTable: React.FC = () => {
  const [modelFilter, setModelFilter] = useState<string>('all');
  const [nodesFilter, setNodesFilter] = useState<string>('all');
  const [budgetFilter, setBudgetFilter] = useState<string>('all');
  const [sortField, setSortField] = useState<keyof FactorialBenchmarkRow>('avgLatencyMean');
  const [sortAsc, setSortAsc] = useState<boolean>(true);

  const filtered = FACTORIAL_SUMMARY_DATA.filter((row) => {
    if (modelFilter !== 'all' && row.topologyModel !== modelFilter) return false;
    if (nodesFilter !== 'all' && row.nodeCount.toString() !== nodesFilter) return false;
    if (budgetFilter !== 'all' && row.controllerBudget.toString() !== budgetFilter)
      return false;
    return true;
  });

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

  const handleExportCSV = () => {
    const headers = [
      'institution',
      'student_number',
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
      'UNIZULU_CS_HONS',
      '230011908',
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
    link.setAttribute('download', `UNIZULU_230011908_Factorial_Benchmark.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-6 flex flex-col">
      {/* Header & SPSS Export Action */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-5 mb-5 border-b border-slate-200">
        <div>
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600 mb-1">
            <span className="font-semibold text-[#0061AF]">
              Section 8.3 &amp; 8.5 Factorial Experimental Ledger
            </span>
            <span aria-hidden="true">·</span>
            <span>SPSS / GENSTAT Departmental Verification Ready</span>
            <span aria-hidden="true">·</span>
            <span>Seed = 42, 142, 242</span>
          </div>
          <h3 className="font-bold text-slate-900 text-lg tracking-tight">
            Multi-Topology Factorial Latency-Cost Matrix
          </h3>
        </div>

        <button
          onClick={handleExportCSV}
          className="flex items-center gap-2 px-4 py-2 rounded-md text-xs font-semibold bg-[#0061AF] hover:bg-[#004987] text-white transition-colors whitespace-nowrap shrink-0"
        >
          <Download className="w-3.5 h-3.5" />
          Download CSV Ledger
        </button>
      </div>

      {/* Interactive Filter Controls */}
      <div className="flex flex-wrap items-center gap-4 mb-5 bg-[#F8FAFC] p-3.5 rounded-md border border-slate-200 text-xs">
        <div className="flex items-center gap-2">
          <label htmlFor="filter-topology" className="text-slate-600 font-medium">
            Topology Family:
          </label>
          <select
            id="filter-topology"
            value={modelFilter}
            onChange={(e) => setModelFilter(e.target.value)}
            className="bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-medium focus:outline-none focus:border-[#0061AF]"
          >
            <option value="all">All Topology Models</option>
            <option value="barabasi_albert">Barabási-Albert (Scale-Free)</option>
            <option value="waxman">Waxman (Geographic)</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="filter-scale" className="text-slate-600 font-medium">
            Node Scale (N):
          </label>
          <select
            id="filter-scale"
            value={nodesFilter}
            onChange={(e) => setNodesFilter(e.target.value)}
            className="bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-medium focus:outline-none focus:border-[#0061AF]"
          >
            <option value="all">All Scales</option>
            <option value="20">N = 20 Nodes</option>
            <option value="50">N = 50 Nodes</option>
            <option value="100">N = 100 Nodes</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="filter-budget" className="text-slate-600 font-medium">
            Controller Budget (k):
          </label>
          <select
            id="filter-budget"
            value={budgetFilter}
            onChange={(e) => setBudgetFilter(e.target.value)}
            className="bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-medium focus:outline-none focus:border-[#0061AF]"
          >
            <option value="all">All Budgets</option>
            <option value="3">k = 3 Controllers</option>
            <option value="5">k = 5 Controllers</option>
          </select>
        </div>

        <span className="ml-auto text-slate-600 font-mono tabular-nums">
          Displaying <strong>{sorted.length}</strong> of {FACTORIAL_SUMMARY_DATA.length} cells
        </span>
      </div>

      {/* Tabular Data Grid — No Row Dot Scatter, Strict Tabular Numerals */}
      <div className="overflow-x-auto rounded-md border border-slate-200">
        <table className="w-full text-left text-xs text-slate-800">
          <thead className="bg-[#F8FAFC] text-slate-600 font-semibold border-b border-slate-200">
            <tr>
              <th className="py-3 px-3.5">Topology Model</th>
              <th className="py-3 px-2.5">Nodes (N)</th>
              <th className="py-3 px-2.5">Budget (k)</th>
              <th className="py-3 px-3.5">Algorithm</th>
              <th
                onClick={() => handleSort('avgLatencyMean')}
                className="py-3 px-3.5 cursor-pointer hover:text-[#0061AF] transition-colors"
              >
                <div className="flex items-center gap-1 whitespace-nowrap">
                  Mean Latency (ms)
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('runtimeMsMean')}
                className="py-3 px-3.5 cursor-pointer hover:text-[#0061AF] transition-colors"
              >
                <div className="flex items-center gap-1 whitespace-nowrap">
                  Runtime (ms)
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('iterationsToConvergeMean')}
                className="py-3 px-3.5 cursor-pointer hover:text-[#0061AF] transition-colors"
              >
                <div className="flex items-center gap-1 whitespace-nowrap">
                  Conv. Epochs
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('latencyGainVsRandomPct')}
                className="py-3 px-3.5 cursor-pointer hover:text-[#0061AF] transition-colors"
              >
                <div className="flex items-center gap-1 whitespace-nowrap">
                  Gain vs. Random
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort('efficiencyRank')}
                className="py-3 px-2.5 cursor-pointer hover:text-[#0061AF] transition-colors"
              >
                <div className="flex items-center gap-1 whitespace-nowrap">
                  Eff. Rank
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th className="py-3 px-3.5">Pareto State</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 font-mono tabular-nums">
            {sorted.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-50 transition-colors">
                <td className="py-2.5 px-3.5 font-sans capitalize text-slate-900">
                  {row.topologyModel.replace('_', '-')}
                </td>
                <td className="py-2.5 px-2.5 text-slate-600">{row.nodeCount}</td>
                <td className="py-2.5 px-2.5 text-[#0061AF] font-semibold">
                  {row.controllerBudget}
                </td>
                <td className="py-2.5 px-3.5 font-sans font-semibold text-slate-900">
                  {row.algorithm === 'greedy_k_center'
                    ? 'Greedy k-Center'
                    : row.algorithm === 'bandit_rl'
                    ? 'AP-DQN / Bandit RL'
                    : row.algorithm === 'genetic'
                    ? 'Genetic Algorithm'
                    : row.algorithm === 'kmeans'
                    ? 'k-Means Clustering'
                    : 'Random Baseline'}
                </td>
                <td className="py-2.5 px-3.5 text-slate-900 font-semibold">
                  {row.avgLatencyMean.toFixed(2)}
                  {row.avgLatencyStd > 0 && (
                    <span className="text-[11px] text-slate-500 ml-1">
                      ±{row.avgLatencyStd.toFixed(2)}
                    </span>
                  )}
                </td>
                <td className="py-2.5 px-3.5 text-slate-700">
                  {row.runtimeMsMean < 1 ? '< 0.50' : row.runtimeMsMean.toFixed(2)}
                </td>
                <td className="py-2.5 px-3.5 text-slate-600">
                  {row.iterationsToConvergeMean.toFixed(1)}
                </td>
                <td
                  className={`py-2.5 px-3.5 font-semibold ${
                    row.latencyGainVsRandomPct > 0 ? 'text-emerald-700' : 'text-slate-500'
                  }`}
                >
                  {row.latencyGainVsRandomPct > 0
                    ? `+${row.latencyGainVsRandomPct.toFixed(2)}%`
                    : '0.00%'}
                </td>
                <td className="py-2.5 px-2.5 font-semibold text-[#844349]">
                  #{row.efficiencyRank}
                </td>
                <td className="py-2.5 px-3.5 font-sans">
                  {row.isParetoOptimal ? (
                    <span className="text-[#0061AF] font-semibold">● Optimal</span>
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
  );
};
