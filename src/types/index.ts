export type TopologyFamily = 'internet2' | 'att_mpls' | 'barabasi_albert' | 'waxman' | 'multi_site_mesh';

export type AlgorithmType = 'random' | 'greedy_k_center' | 'kmeans' | 'genetic' | 'bandit_rl';

export interface GraphNode {
  id: string;
  label: string;
  site?: number;
  x: number;
  y: number;
  isController?: boolean;
  assignedController?: string | null;
  minDistanceToController?: number;
  isReachable?: boolean;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  weight: number; // latency / distance in ms
  linkType?: 'intra_site' | 'inter_site' | 'backbone';
  isFailed?: boolean;
}

export interface NetworkGraph {
  name: string;
  family: TopologyFamily;
  nodes: GraphNode[];
  edges: GraphEdge[];
  nodeCount: number;
  edgeCount: number;
  siteCount: number;
}

export interface PlacementMetrics {
  averageDistance: number;
  worstCaseDistance: number;
  controllerLoadStd: number;
  resilienceRatio: number;
  controlPlaneReliability: number;
  runtimeMs: number;
  iterationsToConverge?: number;
  iterationsBudget?: number;
}

export interface AlgorithmResult {
  algorithm: AlgorithmType;
  algorithmName: string;
  controllers: string[];
  metrics: PlacementMetrics;
  history?: {
    iteration: number;
    bestScore: number;
    epsilon?: number;
  }[];
  isParetoOptimal?: boolean;
  idealPointDistance?: number;
  compromiseRank?: number;
}

export interface FactorialBenchmarkRow {
  topologyModel: string;
  nodeCount: number;
  controllerBudget: number;
  algorithm: string;
  avgLatencyMean: number;
  avgLatencyStd: number;
  runtimeMsMean: number;
  runtimeMsStd: number;
  iterationsBudgetMean: number;
  iterationsToConvergeMean: number;
  latencyRuntimeProduct: number;
  latencyGainVsRandomPct: number;
  efficiencyScore: number;
  efficiencyRank: number;
  isParetoOptimal: boolean;
}

export interface SimulationState {
  failedControllers: Set<string>;
  failedEdges: Set<string>;
}
