import React, { useState } from 'react';
import { AlgorithmResult } from '../types';

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
  const [viewMode, setViewMode] = useState<'latency_reliability' | 'latency_runtime'>(
    'latency_reliability'
  );

  if (results.length === 0) return null;

  const width = 720;
  const height = 370;
  const padding = { top: 42, right: 48, bottom: 54, left: 68 };
  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;

  const latencies = results
    .map((r) => r.metrics.averageDistance)
    .filter((v) => Number.isFinite(v));
  const minLat = Math.max(0, Math.min(...latencies) * 0.85);
  const maxLat = Math.max(...latencies) * 1.15 || 10;

  const reliabilities = results.map((r) => r.metrics.controlPlaneReliability * 100);
  const minRel = Math.max(0, Math.min(...reliabilities) * 0.95);
  const maxRel = 100;

  const runtimes = results.map((r) => Math.max(0.01, r.metrics.runtimeMs));
  const minRuntime = 0;
  const maxRuntime = Math.max(...runtimes) * 1.2 || 100;

  const scaleX = (val: number) =>
    padding.left + ((val - minLat) / (maxLat - minLat || 1)) * innerWidth;
  const scaleYRel = (val: number) =>
    padding.top + innerHeight - ((val - minRel) / (maxRel - minRel || 1)) * innerHeight;
  const scaleYRuntime = (val: number) =>
    padding.top +
    innerHeight -
    ((val - minRuntime) / (maxRuntime - minRuntime || 1)) * innerHeight;

  const paretoPoints = results
    .filter((r) => r.isParetoOptimal && Number.isFinite(r.metrics.averageDistance))
    .sort((a, b) => a.metrics.averageDistance - b.metrics.averageDistance);

  const frontierPath = paretoPoints
    .map((p, idx) => {
      const x = scaleX(p.metrics.averageDistance);
      const y =
        viewMode === 'latency_reliability'
          ? scaleYRel(p.metrics.controlPlaneReliability * 100)
          : scaleYRuntime(p.metrics.runtimeMs);
      return `${idx === 0 ? 'M' : 'L'} ${x} ${y}`;
    })
    .join(' ');

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-6 flex flex-col">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-5 border-b border-slate-200">
        <div>
          <div className="text-xs text-[#0061AF] font-semibold mb-1">
            Multi-Objective Combinatorial Optimization (MOCO) · Section 7 &amp; 8.5
          </div>
          <h3 className="font-bold text-slate-900 text-lg tracking-tight">
            Non-Dominated Pareto Frontier &amp; Ideal-Point Distance Analysis
          </h3>
        </div>

        {/* Interactive Axis View Selector */}
        <div className="flex items-center gap-1 p-1 bg-slate-100 rounded-md border border-slate-200 text-xs">
          <button
            onClick={() => setViewMode('latency_reliability')}
            className={`px-3 py-1.5 rounded font-medium transition-colors whitespace-nowrap shrink-0 ${
              viewMode === 'latency_reliability'
                ? 'bg-[#0061AF] text-white shadow-xs'
                : 'text-slate-700 hover:text-slate-900'
            }`}
          >
            Latency vs. N-1 Reliability
          </button>
          <button
            onClick={() => setViewMode('latency_runtime')}
            className={`px-3 py-1.5 rounded font-medium transition-colors whitespace-nowrap shrink-0 ${
              viewMode === 'latency_runtime'
                ? 'bg-[#0061AF] text-white shadow-xs'
                : 'text-slate-700 hover:text-slate-900'
            }`}
          >
            Latency vs. Computational Cost
          </button>
        </div>
      </div>

      {/* SVG Plot */}
      <div className="w-full bg-[#FAFBFD] border border-slate-200 rounded-md p-3 overflow-x-auto">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto min-w-[540px]">
          {/* Coordinate Grid */}
          {[0, 0.25, 0.5, 0.75, 1].map((pct, idx) => {
            const y = padding.top + pct * innerHeight;
            const x = padding.left + pct * innerWidth;
            return (
              <g key={idx}>
                <line
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                  stroke="#E2E8F0"
                  strokeDasharray="3 3"
                />
                <line
                  x1={x}
                  y1={padding.top}
                  x2={x}
                  y2={height - padding.bottom}
                  stroke="#E2E8F0"
                  strokeDasharray="3 3"
                />
              </g>
            );
          })}

          {/* Axes */}
          <line
            x1={padding.left}
            y1={height - padding.bottom}
            x2={width - padding.right}
            y2={height - padding.bottom}
            stroke="#475569"
            strokeWidth="1.5"
          />
          <line
            x1={padding.left}
            y1={padding.top}
            x2={padding.left}
            y2={height - padding.bottom}
            stroke="#475569"
            strokeWidth="1.5"
          />

          {/* Axis Labels */}
          <text
            x={width / 2}
            y={height - 12}
            textAnchor="middle"
            fill="#334155"
            fontSize="12"
            fontWeight="600"
          >
            Average Controller-Switch Latency (ms) → [Minimize]
          </text>

          <text
            x={-height / 2}
            y={20}
            transform="rotate(-90)"
            textAnchor="middle"
            fill="#334155"
            fontSize="12"
            fontWeight="600"
          >
            {viewMode === 'latency_reliability'
              ? 'Control Plane Survivability (%) → [Maximize]'
              : 'Computational Runtime Cost (ms) → [Minimize]'}
          </text>

          {/* X Tick Values */}
          {[minLat, (minLat + maxLat) / 2, maxLat].map((val, idx) => (
            <text
              key={idx}
              x={scaleX(val)}
              y={height - padding.bottom + 18}
              textAnchor="middle"
              fill="#475569"
              fontSize="10.5"
              fontFamily="IBM Plex Mono, monospace"
            >
              {val.toFixed(2)} ms
            </text>
          ))}

          {/* Y Tick Values */}
          {viewMode === 'latency_reliability'
            ? [minRel, (minRel + maxRel) / 2, maxRel].map((val, idx) => (
                <text
                  key={idx}
                  x={padding.left - 10}
                  y={scaleYRel(val) + 4}
                  textAnchor="end"
                  fill="#475569"
                  fontSize="10.5"
                  fontFamily="IBM Plex Mono, monospace"
                >
                  {val.toFixed(1)}%
                </text>
              ))
            : [minRuntime, (minRuntime + maxRuntime) / 2, maxRuntime].map((val, idx) => (
                <text
                  key={idx}
                  x={padding.left - 10}
                  y={scaleYRuntime(val) + 4}
                  textAnchor="end"
                  fill="#475569"
                  fontSize="10.5"
                  fontFamily="IBM Plex Mono, monospace"
                >
                  {val.toFixed(1)} ms
                </text>
              ))}

          {/* Pareto Frontier Curve */}
          {paretoPoints.length > 1 && (
            <path
              d={frontierPath}
              fill="none"
              stroke="#0061AF"
              strokeWidth="2.5"
              strokeDasharray="5 3"
            />
          )}

          {/* Ideal Point Reference (L_min, R_max) */}
          {viewMode === 'latency_reliability' && (
            <g transform={`translate(${scaleX(minLat)}, ${scaleYRel(maxRel)})`}>
              <circle r="7" fill="#FFF200" stroke="#231F20" strokeWidth="1.5" />
              <circle r="2.5" fill="#231F20" />
              <text
                x="11"
                y="4"
                fill="#0F172A"
                fontSize="10.5"
                fontWeight="700"
                fontFamily="IBM Plex Mono, monospace"
              >
                Ideal Anchor (L_min, R_max)
              </text>
            </g>
          )}

          {/* Algorithm Data Points */}
          {results.map((res) => {
            const x = scaleX(res.metrics.averageDistance);
            const y =
              viewMode === 'latency_reliability'
                ? scaleYRel(res.metrics.controlPlaneReliability * 100)
                : scaleYRuntime(res.metrics.runtimeMs);

            const isSelected = selectedAlgorithmId === res.algorithm;
            const isPareto = res.isParetoOptimal;

            const pointColor = isPareto
              ? '#0061AF' // UNIZULU Blue for Pareto-Optimal
              : res.algorithm === 'bandit_rl'
              ? '#844349' // UNIZULU Burgundy
              : '#64748B';

            return (
              <g
                key={res.algorithm}
                className="cursor-pointer"
                onClick={() => onSelectAlgorithm?.(res)}
              >
                {isSelected && (
                  <circle
                    cx={x}
                    cy={y}
                    r="17"
                    fill="none"
                    stroke="#844349"
                    strokeWidth="2"
                    strokeDasharray="3 2"
                  />
                )}

                {isPareto && (
                  <circle
                    cx={x}
                    cy={y}
                    r="12"
                    fill="rgba(0, 97, 175, 0.14)"
                    stroke="#0061AF"
                    strokeWidth="1.2"
                  />
                )}

                <circle
                  cx={x}
                  cy={y}
                  r={isPareto ? 7.5 : 6}
                  fill={pointColor}
                  stroke="#FFFFFF"
                  strokeWidth="2"
                />

                {res.compromiseRank === 1 && (
                  <circle cx={x} cy={y} r="3" fill="#FFF200" />
                )}

                <text
                  x={x}
                  y={y - 13}
                  textAnchor="middle"
                  fill={isPareto ? '#004987' : '#334155'}
                  fontSize="11"
                  fontWeight={isPareto ? '700' : '600'}
                >
                  {res.algorithm === 'greedy_k_center'
                    ? 'Greedy k-Center'
                    : res.algorithm === 'genetic'
                    ? 'Genetic (GA)'
                    : res.algorithm === 'bandit_rl'
                    ? 'AP-DQN / RL'
                    : res.algorithm === 'kmeans'
                    ? 'k-Means'
                    : 'Random'}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Analytical Decision Interpretation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6 pt-5 border-t border-slate-200 text-xs">
        <div>
          <h4 className="font-bold text-slate-900 mb-1">
            Non-Dominated Pareto Set Identification (RQ2)
          </h4>
          <p className="text-slate-600 leading-relaxed">
            Solutions connected along the dashed UNIZULU Blue frontier ({paretoPoints.map((p) => p.algorithmName.split(' ')[0]).join(', ')}) are Pareto-optimal: no competing algorithm improves latency without degrading control-plane survivability or increasing computational runtime cost.
          </p>
        </div>

        <div>
          <h4 className="font-bold text-[#844349] mb-1">
            Operational Decision Guidance (UNIZULU CS Benchmark Verdict)
          </h4>
          <p className="text-slate-600 leading-relaxed">
            For rapid online failover and dynamic topology reconfiguration, <strong>Greedy k-Center</strong> achieves sub-millisecond execution (&lt;0.5 ms) while capturing 80–88% of meta-heuristic latency gains. For static offline WAN planning, <strong>Genetic Algorithm</strong> and <strong>AP-DQN</strong> minimize steady-state propagation delay.
          </p>
        </div>
      </div>
    </div>
  );
};
