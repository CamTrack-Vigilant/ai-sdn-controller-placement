import React, { useState, useRef } from 'react';
import { NetworkGraph, GraphNode, GraphEdge } from '../types';
import { RefreshCw, ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';

interface TopologyViewProps {
  graph: NetworkGraph;
  activeControllers: string[];
  failedEdges: Set<string>;
  failedControllers: Set<string>;
  onToggleEdgeFailure: (edgeId: string) => void;
  onToggleControllerFailure: (nodeId: string) => void;
  onResetFailures: () => void;
}

// Official UNIZULU & complementary scientific cluster colors
const CONTROLLER_PALETTE = [
  { border: '#0061AF', bg: 'rgba(0, 97, 175, 0.14)', text: '#004987' }, // UNIZULU Blue
  { border: '#844349', bg: 'rgba(132, 67, 73, 0.14)', text: '#683237' }, // UNIZULU Burgundy
  { border: '#D97706', bg: 'rgba(217, 119, 6, 0.16)', text: '#B45309' }, // UNIZULU Heraldic Gold/Amber
  { border: '#0D9488', bg: 'rgba(13, 148, 136, 0.14)', text: '#0F766E' }, // Deep Teal
  { border: '#4F46E5', bg: 'rgba(79, 70, 229, 0.14)', text: '#3730A3' }, // Indigo
  { border: '#231F20', bg: 'rgba(35, 31, 32, 0.12)', text: '#231F20' }, // Heraldic Sable
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
  const workingControllers = activeControllers.filter((c) => !failedControllers.has(c));
  const controllerColorMap = new Map<string, (typeof CONTROLLER_PALETTE)[0]>();
  workingControllers.forEach((c, idx) => {
    controllerColorMap.set(c, CONTROLLER_PALETTE[idx % CONTROLLER_PALETTE.length]);
  });

  // Calculate nearest working controller for each node
  const nodeControllerAssignment = new Map<string, string>();
  for (const node of graph.nodes) {
    if (workingControllers.includes(node.id)) {
      nodeControllerAssignment.set(node.id, node.id);
    } else if (workingControllers.length > 0) {
      let closest = workingControllers[0];
      let minD = Infinity;
      for (const cId of workingControllers) {
        const cNode = graph.nodes.find((n) => n.id === cId);
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

  const svgWidth = 840;
  const svgHeight = 460;

  return (
    <div className="flex flex-col bg-white border border-slate-200 rounded-lg overflow-hidden">
      {/* Topology Header Bar — Zero-Pill Metadata */}
      <div className="px-5 py-3.5 bg-[#F8FAFC] border-b border-slate-200 flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600">
          <h3 className="font-bold text-slate-900 text-sm tracking-tight">{graph.name}</h3>
          <span aria-hidden="true">·</span>
          <span className="font-mono tabular-nums">{graph.nodes.length} switches</span>
          <span aria-hidden="true">·</span>
          <span className="font-mono tabular-nums">{graph.edges.length} links</span>
          <span aria-hidden="true">·</span>
          <span className="font-mono tabular-nums text-[#0061AF] font-semibold">
            k = {activeControllers.length} controllers
          </span>
        </div>

        {/* Viewport & Fault Reset Controls */}
        <div className="flex items-center gap-2">
          {(failedEdges.size > 0 || failedControllers.size > 0) && (
            <button
              onClick={onResetFailures}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded bg-[#ED1C24] text-white hover:bg-red-700 transition-colors whitespace-nowrap shrink-0"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Restore {failedEdges.size + failedControllers.size} Fault
              {failedEdges.size + failedControllers.size > 1 ? 's' : ''}
            </button>
          )}

          <div className="flex items-center bg-white rounded border border-slate-200 p-0.5">
            <button
              onClick={() => setZoom((z) => Math.min(2.4, z + 0.15))}
              className="p-1.5 text-slate-600 hover:text-[#0061AF] hover:bg-slate-50 rounded transition-colors"
              title="Zoom In"
              aria-label="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoom((z) => Math.max(0.55, z - 0.15))}
              className="p-1.5 text-slate-600 hover:text-[#0061AF] hover:bg-slate-50 rounded transition-colors"
              title="Zoom Out"
              aria-label="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={resetZoomPan}
              className="p-1.5 text-slate-600 hover:text-[#0061AF] hover:bg-slate-50 rounded transition-colors"
              title="Reset Viewport"
              aria-label="Reset Viewport"
            >
              <Maximize2 className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Interactive Fault Injection Instruction Bar */}
      <div className="px-5 py-2 bg-[#EBF4FC] border-b border-[#0061AF]/20 flex flex-wrap items-center justify-between gap-2 text-xs text-[#004987]">
        <span>
          <strong>Interactive N-1 Survivability Testbed:</strong> Click any network link to sever/restore fiber connectivity, or click any controller node to trigger an N-1 controller outage.
        </span>
        <span className="font-mono text-[11px] text-slate-600 hidden sm:inline">
          Drag canvas to pan · Click elements to inject faults
        </span>
      </div>

      {/* Main SVG Scientific Coordinate Canvas */}
      <div
        ref={containerRef}
        className="w-full h-[460px] bg-[#FAFBFD] cursor-crosshair relative overflow-hidden select-none"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full h-full">
          <defs>
            <pattern id="unizuluGrid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="rgba(148, 163, 184, 0.22)"
                strokeWidth="0.8"
              />
            </pattern>
          </defs>

          <rect width={svgWidth} height={svgHeight} fill="url(#unizuluGrid)" />

          <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
            {/* 1. Links / Edges */}
            {graph.edges.map((edge) => {
              const srcNode = graph.nodes.find((n) => n.id === edge.source);
              const tgtNode = graph.nodes.find((n) => n.id === edge.target);
              if (!srcNode || !tgtNode) return null;

              const isFailed = failedEdges.has(edge.id);
              const isHovered = hoveredEdge?.id === edge.id;

              return (
                <g
                  key={edge.id}
                  className="cursor-pointer"
                  onClick={() => onToggleEdgeFailure(edge.id)}
                >
                  {/* Invisible wider click target */}
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

                  {/* Visual Link */}
                  <line
                    x1={srcNode.x}
                    y1={srcNode.y}
                    x2={tgtNode.x}
                    y2={tgtNode.y}
                    stroke={
                      isFailed
                        ? '#ED1C24'
                        : isHovered
                        ? '#0061AF'
                        : edge.linkType === 'backbone'
                        ? '#64748B'
                        : '#94A3B8'
                    }
                    strokeWidth={
                      isFailed ? 2.5 : isHovered ? 2.6 : edge.linkType === 'backbone' ? 2.0 : 1.5
                    }
                    strokeDasharray={isFailed ? '5 4' : 'none'}
                  />

                  {/* Fault Marker or Hover Weight Readout */}
                  {isFailed ? (
                    <g
                      transform={`translate(${(srcNode.x + tgtNode.x) / 2}, ${
                        (srcNode.y + tgtNode.y) / 2
                      })`}
                    >
                      <circle r="8" fill="#ED1C24" stroke="#FFFFFF" strokeWidth="1.5" />
                      <line x1="-3" y1="-3" x2="3" y2="3" stroke="#FFFFFF" strokeWidth="1.8" />
                      <line x1="3" y1="-3" x2="-3" y2="3" stroke="#FFFFFF" strokeWidth="1.8" />
                    </g>
                  ) : (
                    isHovered && (
                      <g
                        transform={`translate(${(srcNode.x + tgtNode.x) / 2}, ${
                          (srcNode.y + tgtNode.y) / 2
                        })`}
                      >
                        <rect
                          x="-26"
                          y="-11"
                          width="52"
                          height="20"
                          rx="3"
                          fill="#FFFFFF"
                          stroke="#0061AF"
                          strokeWidth="1.2"
                        />
                        <text
                          x="0"
                          y="3"
                          textAnchor="middle"
                          fill="#0061AF"
                          fontSize="10"
                          fontWeight="600"
                          fontFamily="IBM Plex Mono, monospace"
                        >
                          {edge.weight.toFixed(1)} ms
                        </text>
                      </g>
                    )
                  )}
                </g>
              );
            })}

            {/* 2. Nodes (Switches & Controllers) */}
            {graph.nodes.map((node) => {
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
                  {/* Active Controller Domain Ring */}
                  {isController && !isFailedController && (
                    <>
                      <circle
                        r="21"
                        fill={colorInfo?.bg || 'rgba(0, 97, 175, 0.14)'}
                      />
                      <circle
                        r="15"
                        fill="none"
                        stroke={colorInfo?.border || '#0061AF'}
                        strokeWidth="1.6"
                        strokeDasharray="3 2"
                      />
                    </>
                  )}

                  {/* Crashed Controller Ring */}
                  {isController && isFailedController && (
                    <circle
                      r="18"
                      fill="rgba(237, 28, 36, 0.14)"
                      stroke="#ED1C24"
                      strokeWidth="1.8"
                      strokeDasharray="4 2"
                    />
                  )}

                  {/* Main Node Body */}
                  <circle
                    r={isController ? 10.5 : 6.5}
                    fill={
                      isFailedController
                        ? '#ED1C24'
                        : isController
                        ? colorInfo?.border || '#0061AF'
                        : colorInfo?.border || '#475569'
                    }
                    fillOpacity={isController ? 1 : 0.85}
                    stroke={isHovered ? '#231F20' : '#FFFFFF'}
                    strokeWidth={isHovered ? 2.5 : 1.8}
                  />

                  {/* Controller Gold Bezant Center */}
                  {isController && !isFailedController && (
                    <circle r="4" fill="#FFF200" stroke="#231F20" strokeWidth="1" />
                  )}

                  {/* Node Label */}
                  <text
                    y={isController ? 22 : 16}
                    textAnchor="middle"
                    fill={isController ? '#0F172A' : '#334155'}
                    fontSize={isController ? 11 : 9.5}
                    fontWeight={isController ? '700' : '500'}
                    fontFamily="Plus Jakarta Sans, sans-serif"
                    className="pointer-events-none"
                  >
                    {node.label || node.id}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>

        {/* Hover Node Telemetry Readout */}
        {hoveredNode && (
          <div className="absolute bottom-4 left-4 bg-white/95 border border-slate-300 rounded-md p-3 text-xs shadow-sm text-slate-800 pointer-events-none z-10 min-w-[220px]">
            <div className="flex items-center justify-between pb-1.5 mb-1.5 border-b border-slate-200">
              <span className="font-bold text-[#0061AF]">
                {hoveredNode.label || hoveredNode.id}
              </span>
              <span className="font-mono text-[11px] text-slate-600">
                {activeControllers.includes(hoveredNode.id)
                  ? '● SDN Controller'
                  : '○ OpenFlow Switch'}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-slate-600 font-mono text-[11px] tabular-nums">
              <span>Node Identifier:</span>
              <span className="text-slate-900 font-semibold">{hoveredNode.id}</span>
              <span>Site Partition:</span>
              <span className="text-slate-900">Site {hoveredNode.site ?? 0}</span>
              <span>Primary Authority:</span>
              <span className="text-[#844349] font-semibold">
                {nodeControllerAssignment.get(hoveredNode.id) ?? 'Isolated'}
              </span>
            </div>
          </div>
        )}

        {/* Right Overlay: Active Control Plane Authority Nodes */}
        <div className="absolute top-3 right-3 bg-white/95 border border-slate-200 rounded-md p-3 max-w-[235px] shadow-xs">
          <div className="text-[11px] font-bold text-slate-800 mb-2">
            Control Plane Authorities (Click to Toggle Outage)
          </div>
          <div className="flex flex-col gap-1.5">
            {activeControllers.map((cId) => {
              const node = graph.nodes.find((n) => n.id === cId);
              const isFailed = failedControllers.has(cId);
              const colorInfo = controllerColorMap.get(cId);

              return (
                <button
                  key={cId}
                  onClick={() => onToggleControllerFailure(cId)}
                  className={`flex items-center justify-between px-2.5 py-1.5 rounded text-xs border text-left transition-colors ${
                    isFailed
                      ? 'bg-red-50 border-[#ED1C24]/40 text-[#ED1C24]'
                      : 'bg-slate-50 border-slate-200 text-slate-800 hover:border-[#0061AF]'
                  }`}
                >
                  <span className="truncate font-mono text-[11px] mr-2">
                    {node?.label || cId}
                  </span>
                  <span
                    className="text-[10px] font-mono font-semibold whitespace-nowrap shrink-0"
                    style={{
                      color: isFailed ? '#ED1C24' : colorInfo?.border || '#0061AF',
                    }}
                  >
                    {isFailed ? '✖ Outage' : '● Nominal'}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Legend Footer */}
      <div className="px-5 py-2.5 bg-[#F8FAFC] border-t border-slate-200 flex flex-wrap items-center justify-between text-xs text-slate-600 gap-4">
        <div className="flex items-center gap-5 flex-wrap">
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-full bg-[#0061AF] border-2 border-[#FFF200]" />
            <span>SDN Controller Authority</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-2.5 h-2.5 rounded-full bg-slate-600" />
            <span>Forwarding Switch</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-4 h-0.5 bg-slate-400" />
            <span>Active Optical Link</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-4 h-0.5 border-t-2 border-dashed border-[#ED1C24]" />
            <span>Severed Link (N-1 Fault)</span>
          </div>
        </div>

        <div className="text-[11px] text-slate-500">
          Domain colors indicate minimum-latency controller-switch assignment partitions
        </div>
      </div>
    </div>
  );
};
