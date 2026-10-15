import React from 'react';
import { AlgorithmResult } from '../types';
import { Activity, ShieldCheck, Zap, Scale, Clock, Award, Target, HelpCircle } from 'lucide-react';

interface AlgorithmScorecardProps {
  result: AlgorithmResult;
  baselineResult?: AlgorithmResult;
}

export const AlgorithmScorecard: React.FC<AlgorithmScorecardProps> = ({
  result,
  baselineResult,
}) => {
  const { metrics } = result;

  // Percentage gain compared to baseline (if available)
  const latencyGainPct = baselineResult
    ? ((baselineResult.metrics.averageDistance - metrics.averageDistance) / baselineResult.metrics.averageDistance) * 100
    : null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
      {/* Title & Status */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              Active Solver
            </span>
            <h3 className="font-bold text-slate-100 text-lg">{result.algorithmName}</h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Controllers assigned at nodes: {result.controllers.map(c => `[${c}]`).join(', ')}
          </p>
        </div>

        <div className="flex items-center gap-2">
          {result.isParetoOptimal && (
            <span className="flex items-center gap-1 px-2.5 py-1 text-xs font-bold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              <Award className="w-3.5 h-3.5" />
              Pareto Optimal
            </span>
          )}
          {result.compromiseRank && (
            <span className="flex items-center gap-1 px-2.5 py-1 text-xs font-bold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30">
              <Target className="w-3.5 h-3.5" />
              Compromise Rank #{result.compromiseRank}
            </span>
          )}
        </div>
      </div>

      {/* Grid of Key Benchmark Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {/* 1. Average Latency */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 relative group">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-xs font-medium">Avg Latency</span>
            <Activity className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">
            {Number.isFinite(metrics.averageDistance) ? `${metrics.averageDistance} ms` : '∞'}
          </div>
          {latencyGainPct !== null && (
            <div className={`text-[11px] mt-1 font-semibold ${latencyGainPct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {latencyGainPct >= 0 ? `+${latencyGainPct.toFixed(1)}%` : `${latencyGainPct.toFixed(1)}%`} vs random
            </div>
          )}
        </div>

        {/* 2. Worst-Case Latency */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-xs font-medium">Max Latency</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">
            {Number.isFinite(metrics.worstCaseDistance) ? `${metrics.worstCaseDistance} ms` : '∞'}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">k-center diameter bound</div>
        </div>

        {/* 3. Control Plane Reliability (Single-Link N-1) */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-xs font-medium">N-1 Link Reliability</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">
            {(metrics.controlPlaneReliability * 100).toFixed(1)}%
          </div>
          <div className="text-[11px] text-slate-400 mt-1">reachability under link fault</div>
        </div>

        {/* 4. Resilience Ratio (Controller Crash) */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-xs font-medium">N-1 Controller Resil.</span>
            <Scale className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">
            {metrics.resilienceRatio.toFixed(2)}x
          </div>
          <div className="text-[11px] text-slate-400 mt-1">latency inflation on crash</div>
        </div>

        {/* 5. Load Imbalance */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-xs font-medium">Load Balance Std</span>
            <Scale className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">
            {metrics.controllerLoadStd.toFixed(2)}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">switch allocation variance</div>
        </div>

        {/* 6. Computational Cost */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-xs font-medium">Solver Runtime</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">
            {metrics.runtimeMs < 1 ? '< 1 ms' : `${metrics.runtimeMs} ms`}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            {metrics.iterationsToConverge && metrics.iterationsBudget && metrics.iterationsBudget > 1
              ? `conv. @ ${metrics.iterationsToConverge}/${metrics.iterationsBudget} iters`
              : 'single-pass heuristic'}
          </div>
        </div>
      </div>
    </div>
  );
};
