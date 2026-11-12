import React from 'react';
import { AlgorithmResult } from '../types';

interface AlgorithmScorecardProps {
  result: AlgorithmResult;
  baselineResult?: AlgorithmResult;
  activeFaultCount?: number;
}

export const AlgorithmScorecard: React.FC<AlgorithmScorecardProps> = ({
  result,
  baselineResult,
  activeFaultCount = 0,
}) => {
  const { metrics } = result;

  // Percentage gain compared to random baseline
  const latencyGainPct =
    baselineResult &&
    Number.isFinite(baselineResult.metrics.averageDistance) &&
    Number.isFinite(metrics.averageDistance)
      ? ((baselineResult.metrics.averageDistance - metrics.averageDistance) /
          baselineResult.metrics.averageDistance) *
        100
      : null;

  return (
    <section
      aria-label="Algorithm Multi-Objective Telemetry Scorecard"
      className="bg-white border border-slate-200 rounded-lg p-6"
    >
      {/* Header Row — Zero-Pill Metadata Discipline */}
      <div className="flex flex-wrap items-baseline justify-between gap-4 pb-5 mb-5 border-b border-slate-200">
        <div>
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600 mb-1">
            <span className="font-semibold text-[#0061AF]">Active Placement Policy</span>
            <span aria-hidden="true">·</span>
            <span>
              {result.isParetoOptimal
                ? '● Pareto-Optimal Frontier Member'
                : '○ Dominated Configuration'}
            </span>
            {result.compromiseRank && (
              <>
                <span aria-hidden="true">·</span>
                <span className="font-mono font-medium text-[#844349]">
                  Compromise Rank #{result.compromiseRank}
                </span>
              </>
            )}
            {activeFaultCount > 0 && (
              <>
                <span aria-hidden="true">·</span>
                <span className="font-semibold text-[#ED1C24]">
                  ▲ Degraded ({activeFaultCount} Injected Fault{activeFaultCount > 1 ? 's' : ''})
                </span>
              </>
            )}
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            {result.algorithmName}
          </h2>
        </div>

        <div className="text-xs text-slate-600 font-mono tabular-nums">
          <span>Assigned Controller Nodes: </span>
          <strong className="text-[#0061AF]">
            {result.controllers.length > 0 ? result.controllers.join(', ') : 'None (All Crashed)'}
          </strong>
        </div>
      </div>

      {/* 6-Column Scientific Instrument Telemetry Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
        {/* 1. Average Latency */}
        <div className="border-r border-slate-100 pr-4 last:border-r-0">
          <div className="text-xs text-slate-500 font-medium mb-1">
            Mean Control Latency
          </div>
          <div className="flex items-baseline">
            <span className="text-2xl font-mono font-semibold text-slate-900 tabular-nums">
              {Number.isFinite(metrics.averageDistance)
                ? metrics.averageDistance.toFixed(2)
                : '∞'}
            </span>
            <span className="text-xs font-mono text-slate-500 ml-1.5">ms</span>
          </div>
          {latencyGainPct !== null ? (
            <div
              className={`text-xs font-mono tabular-nums mt-1.5 ${
                latencyGainPct >= 0 ? 'text-emerald-700 font-medium' : 'text-[#ED1C24]'
              }`}
            >
              {latencyGainPct >= 0
                ? `Δ -${latencyGainPct.toFixed(1)}% vs random`
                : `Δ +${Math.abs(latencyGainPct).toFixed(1)}% vs random`}
            </div>
          ) : (
            <div className="text-xs text-slate-500 mt-1.5">Switch-to-controller mean</div>
          )}
        </div>

        {/* 2. Worst-Case Latency */}
        <div className="border-r border-slate-100 pr-4 last:border-r-0">
          <div className="text-xs text-slate-500 font-medium mb-1">
            Worst-Case Latency
          </div>
          <div className="flex items-baseline">
            <span className="text-2xl font-mono font-semibold text-slate-900 tabular-nums">
              {Number.isFinite(metrics.worstCaseDistance)
                ? metrics.worstCaseDistance.toFixed(2)
                : '∞'}
            </span>
            <span className="text-xs font-mono text-slate-500 ml-1.5">ms</span>
          </div>
          <div className="text-xs text-slate-500 mt-1.5">k-center diameter bound</div>
        </div>

        {/* 3. Control Plane Reliability (Single-Link N-1) */}
        <div className="border-r border-slate-100 pr-4 last:border-r-0">
          <div className="text-xs text-slate-500 font-medium mb-1">
            N-1 Link Reliability
          </div>
          <div className="flex items-baseline">
            <span className="text-2xl font-mono font-semibold text-[#0061AF] tabular-nums">
              {(metrics.controlPlaneReliability * 100).toFixed(2)}
            </span>
            <span className="text-xs font-mono text-slate-500 ml-1.5">%</span>
          </div>
          <div className="text-xs text-slate-500 mt-1.5">Single-link fault survivability</div>
        </div>

        {/* 4. Resilience Ratio (Controller Crash) */}
        <div className="border-r border-slate-100 pr-4 last:border-r-0">
          <div className="text-xs text-slate-500 font-medium mb-1">
            Controller Failover Ratio
          </div>
          <div className="flex items-baseline">
            <span className="text-2xl font-mono font-semibold text-slate-900 tabular-nums">
              {Number.isFinite(metrics.resilienceRatio)
                ? metrics.resilienceRatio.toFixed(2)
                : '∞'}
            </span>
            <span className="text-xs font-mono text-slate-500 ml-1.5">×</span>
          </div>
          <div className="text-xs text-slate-500 mt-1.5">N-1 outage delay inflation</div>
        </div>

        {/* 5. Load Balance Standard Deviation */}
        <div className="border-r border-slate-100 pr-4 last:border-r-0">
          <div className="text-xs text-slate-500 font-medium mb-1">
            Load Imbalance (σ)
          </div>
          <div className="flex items-baseline">
            <span className="text-2xl font-mono font-semibold text-slate-900 tabular-nums">
              {metrics.controllerLoadStd.toFixed(2)}
            </span>
            <span className="text-xs font-mono text-slate-500 ml-1.5">nodes</span>
          </div>
          <div className="text-xs text-slate-500 mt-1.5">Switch assignment dispersion</div>
        </div>

        {/* 6. Computational Cost */}
        <div>
          <div className="text-xs text-slate-500 font-medium mb-1">
            Computational Cost
          </div>
          <div className="flex items-baseline">
            <span className="text-2xl font-mono font-semibold text-[#844349] tabular-nums">
              {metrics.runtimeMs < 1 ? '< 1.0' : metrics.runtimeMs.toFixed(1)}
            </span>
            <span className="text-xs font-mono text-slate-500 ml-1.5">ms</span>
          </div>
          <div className="text-xs text-slate-500 font-mono tabular-nums mt-1.5">
            {metrics.iterationsToConverge && metrics.iterationsBudget && metrics.iterationsBudget > 1
              ? `Conv: ${metrics.iterationsToConverge}/${metrics.iterationsBudget} ep`
              : 'Single-pass deterministic'}
          </div>
        </div>
      </div>
    </section>
  );
};
