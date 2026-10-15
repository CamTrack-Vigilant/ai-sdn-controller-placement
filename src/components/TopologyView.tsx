import React, { useState, useRef } from 'react';
import { NetworkGraph, GraphNode, GraphEdge } from '../types';
import { Server, AlertTriangle, RefreshCw, ZoomIn, ZoomOut, Maximize2, ShieldAlert, Cpu } from 'lucide-react';

interface TopologyViewProps {
  graph: NetworkGraph;
  activeControllers: string[];
  failedEdges: Set<string>;
  failedControllers: Set<string>;
  onToggleEdgeFailure: (edgeId: string) => void;
  onToggleControllerFailure: (nodeId: string) => void;
  onResetFailures: () => void;
}

// Visual color palette for controller assignment clusters
const CONTROLLER_PALETTE = [
  { border: '#3b82f6', bg: 'rgba(59, 130, 246, 0.2)', text: '#60a5fa' },
  { border: '#10b981', bg: 'rgba(16, 185, 129, 0.2)', text: '#34d399' },
  { border: '#f59e0b', bg: 'rgba(245, 158, 11, 0.2)', text: '#fbbf24' },
  { border: '#ec4899', bg: 'rgba(236, 72, 153, 0.2)', text: '#f472b6' },
  { border: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.2)', text: '#a78bfa' },
  { border: '#06b6d4', bg: 'rgba(6, 182, 212, 0.2)', text: '#22d3ee' },
];

export const TopologyView: React.FC<TopologyViewProps> = ({
  graph,
  activeControllers,
  failedEdges,
  failedControllers,
  onToggleEdgeFailure,
  onToggleControllerFailure,
  onResetFailures,
}) => {
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [hoveredEdge, setHoveredEdge] = useState<GraphEdge | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);

  // Map each active non-failed controller to a color index
  const workingControllers = activeControllers.filter(c => !failedControllers.has(c));
  const controllerColorMap = new Map<string, typeof CONTROLLER_PALETTE[0]>();
  workingControllers.forEach((c, idx) => {
    controllerColorMap.set(c, CONTROLLER_PALETTE[idx % CONTROLLER_PALETTE.length]);
  });

  // Calculate nearest working controller for each node based on Euclidean position or shortest path
  const nodeControllerAssignment = new Map<string, string>();
  for (const node of graph.nodes) {
    if (workingControllers.includes(node.id)) {
      nodeControllerAssignment.set(node.id, node.id);
    } else if (workingControllers.length > 0) {
      let closest = workingControllers[0];
      let minD = Infinity;
      for (const cId of workingControllers) {
        const cNode = graph.nodes.find(n => n.id === cId);
        if (cNode) {
          const d = Math.sqrt(Math.pow(node.x - cNode.x, 2) + Math.pow(node.y - cNode.y, 2));
          if (d < minD) {
            minD = d;
            closest = cId;
          }
        }
      }
      nodeControllerAssignment.set(node.id, closest);
    }
  }

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button !== 0) return;
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
  };

  const handleMouseUp = () => setIsDragging(false);

  const resetZoomPan = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  // Dimensions
  const svgWidth = 840;
  const svgHeight = 480;

  return (
    <div className="relative flex flex-col bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Topology Header bar */}
      <div className="px-4 py-3 bg-slate-950/80 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></div>
          <span className="font-semibold text-slate-200 text-sm tracking-wide">
            {graph.name}
          </span>
          <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
            {graph.nodes.length} Nodes &middot; {graph.edges.length} Links &middot; {activeControllers.length} Controllers
          </span>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {(failedEdges.size > 0 || failedControllers.size > 0) && (
            <button
              onClick={onResetFailures}
              className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/30 hover:bg-amber-500/20 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Reset {failedEdges.size + failedControllers.size} Faults
            </button>
          )}

          <div className="flex items-center bg-slate-800/80 rounded-lg p-0.5 border border-slate-700">
            <button
              onClick={() => setZoom(z => Math.min(2.5, z + 0.15))}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoom(z => Math.max(0.5, z - 0.15))}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={resetZoomPan}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
              title="Reset View"
            >
              <Maximize2 className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Interactive Guidance Banner */}
      <div className="px-4 py-1.5 bg-cyan-950/30 border-b border-cyan-800/30 flex items-center justify-between text-xs text-cyan-300/80">
        <span className="flex items-center gap-1.5">
          <ShieldAlert className="w-3.5 h-3.5 text-cyan-400" />
          <strong>Failure Injection Mode:</strong> Click any link to simulate single-link failure; click a controller badge to simulate N-1 controller crash.
        </span>
        <span className="text-slate-400 hidden sm:inline">Drag canvas to pan &middot; Scroll to zoom</span>
      </div>

      {/* SVG Canvas */}
      <div
        ref={containerRef}
        className="w-full h-[460px] bg-gradient-to-b from-slate-950 to-slate-900 cursor-grab active:cursor-grabbing relative overflow-hidden select-none"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <svg
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          className="w-full h-full"
        >
          {/* Defs for gradients and glow filters */}
          <defs>
            <radialGradient id="controllerGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0284c7" stopOpacity="0" />
            </radialGradient>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(51, 65, 85, 0.25)" strokeWidth="0.8" />
            </pattern>
          </defs>

          {/* Background Grid */}
          <rect width={svgWidth} height={svgHeight} fill="url(#grid)" />

          <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
            {/* 1. Links / Edges */}
            {graph.edges.map(edge => {
              const srcNode = graph.nodes.find(n => n.id === edge.source);
              const tgtNode = graph.nodes.find(n => n.id === edge.target);
              if (!srcNode || !tgtNode) return null;

              const isFailed = failedEdges.has(edge.id);
              const isHovered = hoveredEdge?.id === edge.id;

              return (
                <g key={edge.id} className="cursor-pointer group" onClick={() => onToggleEdgeFailure(edge.id)}>
                  {/* Invisible thicker hit-box */}
                  <line
                    x1={srcNode.x}
                    y1={srcNode.y}
                    x2={tgtNode.x}
                    y2={tgtNode.y}
                    stroke="transparent"
                    strokeWidth={14}
                    onMouseEnter={() => setHoveredEdge(edge)}
                    onMouseLeave={() => setHoveredEdge(null)}
                  />

                  {/* Visual Line */}
                  <line
                    x1={srcNode.x}
                    y1={srcNode.y}
                    x2={tgtNode.x}
                    y2={tgtNode.y}
                    stroke={
                      isFailed
                        ? '#ef4444'
                        : isHovered
                        ? '#38bdf8'
                        : edge.linkType === 'inter_site'
                        ? '#64748b'
                        : '#334155'
                    }
                    strokeWidth={isFailed ? 2.5 : isHovered ? 2.5 : edge.linkType === 'backbone' ? 2 : 1.5}
                    strokeDasharray={isFailed ? '4 4' : 'none'}
                    className="transition-all duration-200"
                  />

                  {/* Weight / Failure indicator at edge midpoint */}
                  {isFailed ? (
                    <g transform={`translate(${(srcNode.x + tgtNode.x) / 2}, ${(srcNode.y + tgtNode.y) / 2})`}>
                      <circle r="7" fill="#ef4444" />
                      <line x1="-3" y1="-3" x2="3" y2="3" stroke="#fff" strokeWidth="1.5" />
                      <line x1="3" y1="-3" x2="-3" y2="3" stroke="#fff" strokeWidth="1.5" />
                    </g>
                  ) : (
                    isHovered && (
                      <g transform={`translate(${(srcNode.x + tgtNode.x) / 2}, ${(srcNode.y + tgtNode.y) / 2})`}>
                        <rect x="-24" y="-10" width="48" height="20" rx="4" fill="#0f172a" stroke="#38bdf8" strokeWidth="1" />
                        <text x="0" y="3" textAnchor="middle" fill="#38bdf8" fontSize="10" fontFamily="sans-serif">
                          {edge.weight.toFixed(1)}ms
                        </text>
                      </g>
                    )
                  )}
                </g>
              );
            })}

            {/* 2. Nodes */}
            {graph.nodes.map(node => {
              const isController = activeControllers.includes(node.id);
              const isFailedController = failedControllers.has(node.id);
              const assignedCtrl = nodeControllerAssignment.get(node.id);
              const colorInfo = assignedCtrl ? controllerColorMap.get(assignedCtrl) : null;
              const isHovered = hoveredNode?.id === node.id;

              return (
                <g
                  key={node.id}
                  transform={`translate(${node.x}, ${node.y})`}
                  className="cursor-pointer"
                  onClick={() => {
                    if (isController) onToggleControllerFailure(node.id);
                  }}
                  onMouseEnter={() => setHoveredNode(node)}
                  onMouseLeave={() => setHoveredNode(null)}
                >
                  {/* Controller Halo Glow */}
                  {isController && !isFailedController && (
                    <>
                      <circle r="22" fill={colorInfo?.bg || 'rgba(56, 189, 248, 0.2)'} className="animate-pulse" />
                      <circle r="15" fill="none" stroke={colorInfo?.border || '#38bdf8'} strokeWidth="1.5" strokeDasharray="3 3" />
                    </>
                  )}

                  {/* Failed Controller Red Ring */}
                  {isController && isFailedController && (
                    <circle r="18" fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="1.5" strokeDasharray="4 2" />
                  )}

                  {/* Node Circle */}
                  <circle
                    r={isController ? 10 : 6}
                    fill={
                      isFailedController
                        ? '#ef4444'
                        : isController
                        ? colorInfo?.border || '#38bdf8'
                        : colorInfo?.bg
                        ? colorInfo.border
                        : '#475569'
                    }
                    stroke={isHovered ? '#ffffff' : '#0f172a'}
                    strokeWidth={isHovered ? 2 : 1.5}
                    className="transition-colors duration-200"
                  />

                  {/* Controller Icon or Node Label */}
                  {isController ? (
                    <g transform="translate(-5, -5)">
                      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2.5">
                        <rect x="2" y="2" width="20" height="8" rx="2" ry="2" />
                        <rect x="2" y="14" width="20" height="8" rx="2" ry="2" />
                        <line x1="6" y1="6" x2="6.01" y2="6" />
                        <line x1="6" y1="18" x2="6.01" y2="18" />
                      </svg>
                    </g>
                  ) : null}

                  {/* Node Label Text */}
                  <text
                    y={isController ? 20 : 16}
                    textAnchor="middle"
                    fill={isController ? '#e2e8f0' : '#94a3b8'}
                    fontSize={isController ? 11 : 9}
                    fontWeight={isController ? '600' : '400'}
                    fontFamily="system-ui, sans-serif"
                    className="pointer-events-none drop-shadow"
                  >
                    {node.label || node.id}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>

        {/* Hover Information Floating Card */}
        {hoveredNode && (
          <div className="absolute bottom-4 left-4 bg-slate-900/95 border border-slate-700 backdrop-blur-md rounded-lg p-3 text-xs shadow-xl text-slate-200 pointer-events-none z-10 min-w-[200px]">
            <div className="flex items-center justify-between pb-1 mb-1 border-b border-slate-800">
              <span className="font-bold text-cyan-400">{hoveredNode.label || hoveredNode.id}</span>
              {activeControllers.includes(hoveredNode.id) ? (
                <span className="px-1.5 py-0.5 rounded text-[10px] bg-cyan-500/20 text-cyan-300 font-semibold border border-cyan-500/30">
                  Controller
                </span>
              ) : (
                <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400">
                  Switch
                </span>
              )}
            </div>
            <div className="grid grid-cols-2 gap-x-2 gap-y-1 text-slate-400">
              <span>Node ID:</span> <span className="text-slate-200 font-mono">{hoveredNode.id}</span>
              <span>Site Partition:</span> <span className="text-slate-200">Site {hoveredNode.site ?? 0}</span>
              <span>Assigned To:</span>{' '}
              <span className="text-cyan-300 font-mono">
                {nodeControllerAssignment.get(hoveredNode.id) ?? 'None'}
              </span>
            </div>
          </div>
        )}

        {/* Live Controller Status Badges */}
        <div className="absolute top-4 right-4 flex flex-col gap-1.5 bg-slate-950/90 border border-slate-800 backdrop-blur rounded-lg p-2.5 max-w-[220px]">
          <span className="text-[11px] font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-cyan-400" /> Controller Plane
          </span>
          <div className="flex flex-col gap-1">
            {activeControllers.map(cId => {
              const node = graph.nodes.find(n => n.id === cId);
              const isFailed = failedControllers.has(cId);
              const colorInfo = controllerColorMap.get(cId);

              return (
                <div
                  key={cId}
                  onClick={() => onToggleControllerFailure(cId)}
                  className={`flex items-center justify-between px-2 py-1 rounded text-xs cursor-pointer border transition-colors ${
                    isFailed
                      ? 'bg-rose-950/40 border-rose-800/60 text-rose-300 hover:bg-rose-900/50'
                      : 'bg-slate-900/80 border-slate-700/80 text-slate-200 hover:border-slate-500'
                  }`}
                  title={isFailed ? 'Click to restore controller' : 'Click to inject crash fault'}
                >
                  <div className="flex items-center gap-1.5 truncate">
                    <span
                      className="w-2.5 h-2.5 rounded-full inline-block"
                      style={{ backgroundColor: isFailed ? '#ef4444' : colorInfo?.border || '#38bdf8' }}
                    />
                    <span className="truncate font-mono">{node?.label || cId}</span>
                  </div>
                  {isFailed ? (
                    <span className="text-[10px] text-rose-400 font-bold">CRASHED</span>
                  ) : (
                    <span className="text-[10px] text-emerald-400">ACTIVE</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Legend Footer */}
      <div className="px-4 py-2 bg-slate-950/90 border-t border-slate-800/80 flex flex-wrap items-center justify-between text-xs text-slate-400 gap-3">
        <div className="flex items-center gap-4 flex-wrap">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-cyan-500 border border-white"></div>
            <span>SDN Controller</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-slate-500"></div>
            <span>OpenFlow Switch</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-0.5 bg-slate-600"></div>
            <span>Healthy Link</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-0.5 bg-rose-500 border-dashed border-t"></div>
            <span>Injected Link Sever (N-1)</span>
          </div>
        </div>

        <div className="text-[11px] text-slate-400">
          Clustered colors designate closest controller latency domains
        </div>
      </div>
    </div>
  );
};
