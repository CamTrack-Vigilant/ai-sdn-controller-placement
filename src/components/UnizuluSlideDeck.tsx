import React, { useState } from 'react';
import { AlgorithmResult, NetworkGraph } from '../types';
import { UnizuluWaveSvgBackground } from './UnizuluOfficialWave';
import { UnizuluOfficialSeal } from './UnizuluLogo';
import { ChevronLeft, ChevronRight, Eye, Layers } from 'lucide-react';

interface UnizuluSlideDeckProps {
  graph: NetworkGraph;
  results: AlgorithmResult[];
  effectiveBudget: number;
  seed: number;
}

interface SlideDefinition {
  id: number;
  section: string;
  title: string;
  subtitle: string;
  isCover?: boolean;
  bullets?: { heading: string; detail: string }[];
  speakerCue: string;
}

export const UnizuluSlideDeck: React.FC<UnizuluSlideDeckProps> = ({
  graph,
  results,
  effectiveBudget,
  seed,
}) => {
  const [currentSlide, setCurrentSlide] = useState<number>(0);
  const [showOriginalTemplateImage, setShowOriginalTemplateImage] =
    useState<boolean>(false);

  const slides: SlideDefinition[] = [
    {
      id: 1,
      section: 'University of Zululand · BSc Honours R&D Defence',
      title: 'Proposal Stage Plan for R and D',
      subtitle:
        'Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site SDN',
      isCover: true,
      speakerCue:
        'Welcome the panel (Prof. Mudali, Dr. Zwane, and faculty assessors). State clearly that this study is a formal positivist scientific comparison investigating when AI controller placement is operationally justified over classical heuristics.',
    },
    {
      id: 2,
      section: 'Section 1 & 2 · Problem Context & The Decision Crisis',
      title: 'Why Single-Metric SDN Placement Fails in Practice',
      subtitle:
        'Decoupling the Control Plane creates a multi-site placement bottleneck across latency, survivability, and compute cost',
      bullets: [
        {
          heading: '01. The Infrastructure Decision Gap',
          detail:
            'Published SDN studies routinely claim AI superiority based on isolated latency reductions while omitting training and inference burden (Seconds per Episode).',
        },
        {
          heading: '02. Multi-Site Survivability Constraints',
          detail:
            'In geographically distributed backbones (Internet2, AT&T MPLS, SANReN), single-link (N-1) failures can isolate switches from their control authority (Heller et al., 2012; Radam et al., 2022).',
        },
        {
          heading: '03.Unified 3-Axis MOCO Framing',
          detail:
            'This study evaluates Average Latency (ms), Control-Plane Reliability (%), and Computational Cost jointly to identify non-dominated Pareto fronts.',
        },
      ],
      speakerCue:
        'Emphasize that optimizing latency alone can produce fragile or computationally expensive placements that are infeasible for real-time network reconvergence.',
    },
    {
      id: 3,
      section: 'Section 3 & 4 · Research Questions & Deductive Hypotheses',
      title: 'Primary Research Question & Testable Hypotheses',
      subtitle:
        'Deductive hypothesis testing across five method families under identical seeded conditions',
      bullets: [
        {
          heading: 'H1: Latency Performance Superiority',
          detail:
            'Genetic Algorithm (GA) and AP-DQN discover placements with significantly lower mean switch-to-controller latency than Random and Greedy baselines (22.9%–37.1% gain, p < 0.001).',
        },
        {
          heading: 'H2: Computational Efficiency Trade-off',
          detail:
            'Greedy k-Center executes in < 0.5 ms (up to 18,000× faster than RL) while retaining 80–85% of AI latency gains, remaining Pareto-optimal for online failover.',
        },
        {
          heading: 'H3: Topology Family Sensitivity',
          detail:
            'Scale-free Barabási-Albert hubs favor fast degree-seeded heuristics, whereas Waxman geographic dispersion widens the advantage of global evolutionary search.',
        },
      ],
      speakerCue:
        'Show how each hypothesis directly maps to our Golden Thread in Section 8.5.1—linking research questions to ANOVA, effect sizes, and Pareto ranking.',
    },
    {
      id: 4,
      section: 'Section 8.4.1 · Parameter Justification & Technical Stack Defense',
      title: 'Methodological Rigor & Baseline Parity',
      subtitle:
        'Four non-negotiable pillars defending the experimental architecture',
      bullets: [
        {
          heading: '01. Canonical Topology Parity (Heller et al., 2012)',
          detail:
            'Retains Internet2 (11 nodes) and AT&T MPLS (21 nodes) reference backbones alongside Barabási-Albert and Waxman factorial scaling (N ∈ {20, 50, 100}, k ∈ {3, 5}).',
        },
        {
          heading: '02. Auditable N-1 Reliability Operationalization',
          detail:
            'Eliminates black-box reliability scoring by explicitly computing the mean fraction of nodes remaining controller-reachable across all single-edge removals.',
        },
        {
          heading: '03. Validated AP-DQN Pilot (Farahi et al., 2026)',
          detail:
            'Calibrated with lr = 0.001, batch = 32, γ = 0.99, replay = 10,000. Completed 50-episode pilot in 1.13s (0.0226s/episode), proving Honours timeline feasibility.',
        },
      ],
      speakerCue:
        'Highlight that our 0.0226 seconds/episode pilot proof-of-concept removes any execution risk for the full factorial matrix.',
    },
    {
      id: 5,
      section: 'Section 8.5 · Live Experimental Evidence from Workbench',
      title: `Live Benchmark Telemetry: ${graph.name}`,
      subtitle: `Comparative evaluation at Controller Budget k = ${effectiveBudget}, Random Seed = ${seed}`,
      bullets: results.slice(0, 4).map((r, i) => ({
        heading: `0${i + 1}. ${r.algorithmName} ${r.isParetoOptimal ? '(● Pareto-Optimal)' : ''}`,
        detail: `Mean Latency: ${r.metrics.averageDistance.toFixed(2)} ms · Worst-Case: ${r.metrics.worstCaseDistance.toFixed(2)} ms · N-1 Reliability: ${(r.metrics.controlPlaneReliability * 100).toFixed(2)}% · Runtime: ${r.metrics.runtimeMs.toFixed(2)} ms (Rank #${r.compromiseRank ?? '-'})`,
      })),
      speakerCue:
        'Point out that this slide pulls live recalculated values directly from the interactive simulation engine in our workbench.',
    },
    {
      id: 6,
      section: 'Section 11 · R&D Stage Plan & Operational Recommendations',
      title: 'Scenario-Conditioned Decision Guidance',
      subtitle:
        'Actionable engineering rules for multi-site SDN infrastructure teams',
      bullets: [
        {
          heading: 'When to Deploy AI / Meta-Heuristics (GA & AP-DQN)',
          detail:
            'Recommended for offline greenfield WAN architecture design and geographically dispersed Waxman-class backbones where compute time (100–350 ms) is unconstrained.',
        },
        {
          heading: 'When Heuristics Suffice (Greedy k-Center)',
          detail:
            'Recommended for sub-millisecond online controller re-election during link churn or DDoS mitigation, capturing >80% of optimal latency reduction in < 0.5 ms.',
        },
        {
          heading: 'Departmental Reproducibility & SPSS/GENSTAT Audit',
          detail:
            'All 60 factorial scenario cells and seed-stability sweeps (Seeds 42, 142, 242) export directly to standardized CSV ledgers for independent verification.',
        },
      ],
      speakerCue:
        'Conclude with our core takeaway: AI is not a universal replacement for heuristics; engineering maturity lies in knowing the exact Pareto boundary between them.',
    },
  ];

  const activeSlide = slides[currentSlide];

  return (
    <div className="space-y-6">
      {/* Deck Control Toolbar */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600">
          <span className="font-bold text-[#0061AF]">
            Official UNIZULU R&amp;D Presentation Deck
          </span>
          <span aria-hidden="true">·</span>
          <span className="font-mono tabular-nums">
            Slide {currentSlide + 1} of {slides.length}
          </span>
          <span aria-hidden="true">·</span>
          <span>Candidate: Thabang Nhlokoma Buthelezi (230011908)</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowOriginalTemplateImage((prev) => !prev)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium border transition-colors whitespace-nowrap shrink-0 ${
              showOriginalTemplateImage
                ? 'bg-[#84383E] text-white border-[#84383E]'
                : 'bg-[#F8FAFC] text-slate-700 border-slate-300 hover:border-[#0061AF]'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            {showOriginalTemplateImage
              ? 'Viewing Attached Template Reference'
              : 'Compare with Attached Template Image'}
          </button>

          <div className="flex items-center gap-1">
            <button
              onClick={() => setCurrentSlide((s) => Math.max(0, s - 1))}
              disabled={currentSlide === 0}
              className="p-1.5 rounded border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 disabled:opacity-40 transition-colors"
              title="Previous Slide"
              aria-label="Previous Slide"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() =>
                setCurrentSlide((s) => Math.min(slides.length - 1, s + 1))
              }
              disabled={currentSlide === slides.length - 1}
              className="p-1.5 rounded border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 disabled:opacity-40 transition-colors"
              title="Next Slide"
              aria-label="Next Slide"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Optional Reference View of the Exact Attached School Design Image */}
      {showOriginalTemplateImage && (
        <div className="bg-white border border-slate-200 rounded-lg p-5">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-200 text-xs">
            <span className="font-bold text-[#0061AF]">
              Official Attached UNIZULU School Design Template Reference
            </span>
            <span className="text-slate-500 font-mono">
              /assets/aistudio/WhatsApp_Image_2026-11-08_at_22.09.23_6a50b93d.jpeg
            </span>
          </div>
          <div className="max-w-4xl mx-auto overflow-hidden rounded border border-slate-200">
            <img
              src="/assets/aistudio/WhatsApp_Image_2026-11-08_at_22.09.23_6a50b93d.jpeg"
              alt="Official University of Zululand Proposal Stage Plan for R and D Design"
              referrerPolicy="no-referrer"
              className="w-full h-auto object-contain"
            />
          </div>
        </div>
      )}

      {/* 16:9 Official University of Zululand Slide Stage */}
      <div className="relative w-full aspect-16/9 min-h-[460px] rounded-lg overflow-hidden border border-slate-300 shadow-lg bg-[#00468B] text-white select-none">
        {/* Official UNIZULU Wave Vector Canvas */}
        <div className="absolute inset-0 pointer-events-none">
          <UnizuluWaveSvgBackground className="w-full h-full" />
        </div>

        {/* Top-Right Official UNIZULU Coat of Arms in the White Curved Lobe */}
        <div className="absolute top-[3.5%] right-[3.8%] z-20 flex flex-col items-center">
          <UnizuluOfficialSeal size="md" />
        </div>

        {/* Slide Foreground Content */}
        {activeSlide.isCover ? (
          <div className="relative z-10 h-full flex flex-col items-center justify-center text-center px-8 sm:px-20 pb-12">
            <div className="text-xs sm:text-sm font-semibold tracking-wider text-[#FFF200] uppercase mb-3">
              {activeSlide.section}
            </div>
            <h2
              className="text-3xl sm:text-5xl lg:text-[54px] font-normal tracking-tight text-white leading-[1.15] max-w-3xl"
              style={{ textWrap: 'balance' }}
            >
              Proposal Stage Plan for R and D
            </h2>
            <p className="text-lg sm:text-2xl text-white/95 font-normal mt-4">
              Workshop Part 2 · Multi-Objective SDN Controller Placement
            </p>
            <div className="mt-6 pt-4 border-t border-white/25 text-xs sm:text-sm text-blue-100 max-w-2xl">
              <p className="font-semibold text-white">{activeSlide.subtitle}</p>
              <p className="mt-2 font-mono text-xs text-[#FFF200]">
                Thabang Nhlokoma Buthelezi (230011908) · Supervised by Prof. P. Mudali &amp; Dr. S. Zwane
              </p>
            </div>
          </div>
        ) : (
          <div className="relative z-10 h-full flex flex-col justify-between p-6 sm:p-10 lg:p-12">
            {/* Slide Header */}
            <div className="max-w-[72%]">
              <div className="text-xs font-semibold text-[#FFF200] mb-1">
                {activeSlide.section}
              </div>
              <h2 className="text-xl sm:text-3xl font-bold text-white tracking-tight">
                {activeSlide.title}
              </h2>
              <p className="text-xs sm:text-sm text-blue-100 mt-1">
                {activeSlide.subtitle}
              </p>
            </div>

            {/* Slide Body Points */}
            <div className="grid grid-cols-1 gap-3.5 my-auto max-w-[78%] py-4">
              {activeSlide.bullets?.map((b, idx) => (
                <div
                  key={idx}
                  className="bg-[#002B54]/75 backdrop-blur-xs border border-white/20 rounded-md px-4 py-3"
                >
                  <div className="text-xs sm:text-sm font-bold text-[#FFF200] mb-0.5">
                    {b.heading}
                  </div>
                  <p className="text-xs text-white/95 leading-relaxed font-mono tabular-nums">
                    {b.detail}
                  </p>
                </div>
              ))}
            </div>

            {/* Slide Footer Caption */}
            <div className="flex items-center justify-between text-[11px] text-white/80 font-mono pt-2">
              <span>UNIZULU Dept. of Computer Science · Honours R&amp;D</span>
              <span>
                Slide {currentSlide + 1} / {slides.length}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Slide Thumbnail Strip & Speaker Script Notes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-lg p-4">
          <div className="text-xs font-bold text-slate-800 mb-3 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-[#0061AF]" />
            <span>Slide Navigator (Click to Jump)</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
            {slides.map((s, idx) => (
              <button
                key={s.id}
                onClick={() => setCurrentSlide(idx)}
                className={`p-2.5 rounded border text-left transition-colors ${
                  currentSlide === idx
                    ? 'bg-[#EBF4FC] border-[#0061AF] text-[#004987]'
                    : 'bg-[#FAFBFD] border-slate-200 text-slate-700 hover:border-slate-300'
                }`}
              >
                <div className="text-[10px] font-mono font-semibold text-[#84383E]">
                  Slide 0{idx + 1}
                </div>
                <div className="text-xs font-bold truncate mt-0.5">{s.title}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col justify-between">
          <div>
            <div className="text-xs font-bold text-[#84383E] mb-1.5">
              Oral Defence Speaker Cue (Slide {currentSlide + 1})
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {activeSlide.speakerCue}
            </p>
          </div>
          <div className="pt-3 mt-3 border-t border-slate-100 text-[11px] text-slate-500 font-mono">
            Template: Official UNIZULU Blue / Burgundy / Gold Wave Theme
          </div>
        </div>
      </div>
    </div>
  );
};
