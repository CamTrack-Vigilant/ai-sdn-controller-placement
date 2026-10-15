import React, { useState } from 'react';
import { AlgorithmResult } from '../types';
import { Award, Compass, Sparkles, Sliders } from 'lucide-react';

interface ParetoChartProps {
  results: AlgorithmResult[];
  onSelectAlgorithm?: (algo: AlgorithmResult) => void;
  selectedAlgorithmId?: string;
}

export const ParetoChart: React.FC<ParetoChartProps> = ({
  results,
  onSelectAlgorithm,
  selectedAlgorithmId,
}) => {
  const [viewMode, setViewMode] = useState<'latency_reliability' | 'latency_runtime'>('latency_reliability');

  if (results.length === 0) return null;

  // Chart dimensions
  const width = 680;
  const height = 360;
  const padding = { top: 40, right: 40, bottom: 50, left: 60 };
  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;

  // Bounds for axes
  const latencies = results.map(r => r.metrics.averageDistance).filter(v => Number.isFinite(v));
  const minLat = Math.max(0, Math.min(...latencies) * 0.85);
  const maxLat = Math.max(...latencies) * 1.15 || 10;

  const reliabilities = results.map(r => r.metrics.controlPlaneReliability * 100);
  const minRel = Math.max(0, Math.min(...reliabilities) * 0.95);
  const maxRel = 100;

  const runtimes = results.map(r => Math.max(0.01, r.metrics.runtimeMs));
  const minRuntime = 0;
  const maxRuntime = Math.max(...runtimes) * 1.2 || 100;

  // Scales
  const scaleX = (val: number) => padding.left + ((val - minLat) / (maxLat - minLat || 1)) * innerWidth;
  const scaleYRel = (val: number) => padding.top + innerHeight - ((val - minRel) / (maxRel - minRel || 1)) * innerHeight;
  const scaleYRuntime = (val: number) => padding.top + innerHeight - ((val - minRuntime) / (maxRuntime - minRuntime || 1)) * innerHeight;

  // Non-dominated Pareto frontier points
  const paretoPoints = results
    .filter(r => r.isParetoOptimal && Number.isFinite(r.metrics.averageDistance))
    .sort((a, b) => a.metrics.averageDistance - b.metrics.averageDistance);

  // Line points for frontier
  const frontierPath = paretoPoints
    .map((p, idx) => {
      const x = scaleX(p.metrics.averageDistance);
      const y = viewMode === 'latency_reliability'
        ? scaleYRel(p.metrics.controlPlaneReliability * 100)
        : scaleYRuntime(p.metrics.runtimeMs);
      return `${idx === 0 ? 'M' : 'L'} ${x} ${y}`;
    })
    .join(' ');

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex flex-col">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <Compass className="w-5 h-5 text-cyan-400" />
            <h3 className="font-bold text-slate-100 text-base">Multi-Objective Pareto Trade-off Frontier</h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Non-dominated decision boundaries: minimizing latency while maximizing reliability & efficiency
          </p>
        </div>

        <div className="flex items-center bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
          <button
            onClick={() => setViewMode('latency_reliability')}
            className={`px-3 py-1 rounded font-medium transition-colors ${
              viewMode === 'latency_reliability'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Latency vs. Reliability
          </button>
          <button
            onClick={() => setViewMode('latency_runtime')}
            className={`px-3 py-1 rounded font-medium transition-colors ${
              viewMode === 'latency_runtime'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Latency vs. Runtime
          </button>
        </div>
      </div>

      {/* SVG Scatter & Frontier Plot */}
      <div className="w-full bg-slate-950/70 border border-slate-800/80 rounded-lg p-2 overflow-x-auto">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto min-w-[500px]">
          {/* Grid lines */}
          {[0, 0.25, 0.5, 0.75, 1].map((pct, idx) => {
            const y = padding.top + pct * innerHeight;
            const x = padding.left + pct * innerWidth;
            return (
              <g key={idx}>
                {/* Horizontal */}
                <line x1={padding.left} y1={y} x2={width - padding.right} y2={y} stroke="rgba(51, 65, 85, 0.4)" strokeDasharray="3 3" />
                {/* Vertical */}
                <line x1={x} y1={padding.top} x2={x} y2={height - padding.bottom} stroke="rgba(51, 65, 85, 0.4)" strokeDasharray="3 3" />
              </g>
            );
          })}

          {/* Axes Lines */}
          <line
            x1={padding.left}
            y1={height - padding.bottom}
            x2={width - padding.right}
            y2={height - padding.bottom}
            stroke="#64748b"
            strokeWidth="1.5"
          />
          <line
            x1={padding.left}
            y1={padding.top}
            x2={padding.left}
            y2={height - padding.bottom}
            stroke="#64748b"
            strokeWidth="1.5"
          />

          {/* Axis Labels */}
          <text
            x={width / 2}
            y={height - 12}
            textAnchor="middle"
            fill="#94a3b8"
            fontSize="12"
            fontWeight="500"
          >
            Average Controller Latency (ms) → [Lower is Better]
          </text>

          <text
            x={-height / 2}
            y={20}
            transform="rotate(-90)"
            textAnchor="middle"
            fill="#94a3b8"
            fontSize="12"
            fontWeight="500"
          >
            {viewMode === 'latency_reliability'
              ? 'Control Plane Reliability (%) → [Higher is Better]'
              : 'Solver Runtime (ms) → [Lower is Better]'}
          </text>

          {/* X Tick Values */}
          {[minLat, (minLat + maxLat) / 2, maxLat].map((val, idx) => (
            <text
              key={idx}
              x={scaleX(val)}
              y={height - padding.bottom + 18}
              textAnchor="middle"
              fill="#64748b"
              fontSize="10"
              fontFamily="monospace"
            >
              {val.toFixed(1)}
            </text>
          ))}

          {/* Y Tick Values */}
          {viewMode === 'latency_reliability'
            ? [minRel, (minRel + maxRel) / 2, maxRel].map((val, idx) => (
                <text
                  key={idx}
                  x={padding.left - 8}
                  y={scaleYRel(val) + 4}
                  textAnchor="end"
                  fill="#64748b"
                  fontSize="10"
                  fontFamily="monospace"
                >
                  {val.toFixed(0)}%
                </text>
              ))
            : [minRuntime, (minRuntime + maxRuntime) / 2, maxRuntime].map((val, idx) => (
                <text
                  key={idx}
                  x={padding.left - 8}
                  y={scaleYRuntime(val) + 4}
                  textAnchor="end"
                  fill="#64748b"
                  fontSize="10"
                  fontFamily="monospace"
                >
                  {val.toFixed(0)}ms
                </text>
              ))}

          {/* Frontier Line */}
          {paretoPoints.length > 1 && (
            <path
              d={frontierPath}
              fill="none"
              stroke="#06b6d4"
              strokeWidth="2.5"
              strokeDasharray="4 2"
              className="drop-shadow"
            />
          )}

          {/* Ideal Point Marker */}
          {viewMode === 'latency_reliability' && (
            <g transform={`translate(${scaleX(minLat)}, ${scaleYRel(maxRel)})`}>
              <circle r="6" fill="#3b82f6" fillOpacity="0.4" />
              <circle r="3" fill="#60a5fa" />
              <text x="8" y="4" fill="#60a5fa" fontSize="9" fontWeight="bold">
                Ideal Point (L_min, R_max)
              </text>
            </g>
          )}

          {/* Solution Points */}
          {results.map((res) => {
            const x = scaleX(res.metrics.averageDistance);
            const y = viewMode === 'latency_reliability'
              ? scaleYRel(res.metrics.controlPlaneReliability * 100)
              : scaleYRuntime(res.metrics.runtimeMs);

            const isSelected = selectedAlgorithmId === res.algorithm;
            const isPareto = res.isParetoOptimal;

            return (
              <g
                key={res.algorithm}
                className="cursor-pointer transition-transform group"
                onClick={() => onSelectAlgorithm?.(res)}
              >
                {/* Selection Halo */}
                {isSelected && (
                  <circle cx={x} cy={y} r="18" fill="none" stroke="#38bdf8" strokeWidth="2" strokeDasharray="3 3" />
                )}

                {/* Pareto Highlight */}
                {isPareto && (
                  <circle cx={x} cy={y} r="12" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="1" />
                )}

                {/* Main Node Point */}
                <circle
                  cx={x}
                  cy={y}
                  r={isPareto ? 8 : 6}
                  fill={
                    isPareto
                      ? '#10b981'
                      : res.algorithm === 'greedy_k_center'
                      ? '#3b82f6'
                      : res.algorithm === 'genetic'
                      ? '#8b5cf6'
                      : res.algorithm === 'bandit_rl'
                      ? '#f59e0b'
                      : '#64748b'
                  }
                  stroke="#0f172a"
                  strokeWidth="2"
                />

                {/* Point Label */}
                <text
                  cx={x}
                  x={x}
                  y={y - 12}
                  textAnchor="middle"
                  fill={isPareto ? '#34d399' : '#cbd5e1'}
                  fontSize="11"
                  fontWeight={isPareto ? 'bold' : '500'}
                  className="pointer-events-none drop-shadow"
                >
                  {res.algorithm === 'greedy_k_center'
                    ? 'Greedy'
                    : res.algorithm === 'genetic'
                    ? 'GA'
                    : res.algorithm === 'bandit_rl'
                    ? 'Bandit RL'
                    : res.algorithm === 'kmeans'
                    ? 'k-Means'
                    : 'Random'}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Decision Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4 text-xs">
        <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg">
          <div className="flex items-center gap-1.5 font-semibold text-emerald-400 mb-1">
            <Award className="w-3.5 h-3.5" /> Pareto Non-Dominated Set
          </div>
          <p className="text-slate-400 leading-relaxed">
            {paretoPoints.map(p => p.algorithmName.split(' ')[0]).join(', ')} form the efficient boundary. No other configuration can simultaneously achieve lower latency without sacrificing reliability or runtime.
          </p>
        </div>

        <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg">
          <div className="flex items-center gap-1.5 font-semibold text-cyan-400 mb-1">
            <Sparkles className="w-3.5 h-3.5" /> Recommended Trade-off
          </div>
          <p className="text-slate-400 leading-relaxed">
            For online SDN controller failover under link churn, <strong>Greedy k-Center</strong> offers instantaneous reconvergence (&lt;0.5ms). For offline greenfield deployment, <strong>Genetic Algorithm</strong> yields maximum latency reduction.
          </p>
        </div>
      </div>
    </div>
  );
};
