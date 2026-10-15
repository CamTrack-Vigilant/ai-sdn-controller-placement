import React from 'react';
import { RESEARCH_HYPOTHESES, LITERATURE_REFERENCES } from '../data/benchmarkDatasets';
import { CheckCircle2, BookOpen, Layers, GitCompare, FileText, Check } from 'lucide-react';

export const HypothesisDashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Research Questions & Hypotheses */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
        <div className="flex items-center gap-2 pb-3 mb-4 border-b border-slate-800">
          <Layers className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-slate-100 text-base">
            Deductive Research Hypotheses & Empirical Findings
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {RESEARCH_HYPOTHESES.map((h) => (
            <div
              key={h.id}
              className="bg-slate-950/70 border border-slate-800 rounded-lg p-4 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-xs font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                    {h.id}
                  </span>
                  <span className="flex items-center gap-1 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    {h.verdict}
                  </span>
                </div>
                <h4 className="font-bold text-slate-200 text-sm mb-1.5">{h.title}</h4>
                <p className="text-xs text-slate-400 leading-relaxed mb-3">
                  {h.statement}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-800/80 text-xs">
                <div className="font-semibold text-slate-300 mb-1">Empirical Evidence:</div>
                <p className="text-slate-400 text-[11px] leading-relaxed mb-2">
                  {h.evidence}
                </p>
                <div className="text-[11px] font-mono text-cyan-400 bg-cyan-950/40 p-1.5 rounded border border-cyan-800/40">
                  {h.significance}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Literature Foundation & Technical Stack Defense */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
        <div className="flex items-center gap-2 pb-3 mb-4 border-b border-slate-800">
          <BookOpen className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-slate-100 text-base">
            Methodology & Canonical References (IEEE Standard)
          </h3>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {LITERATURE_REFERENCES.map((ref) => (
            <div
              key={ref.id}
              className="bg-slate-950/60 border border-slate-800 rounded-lg p-3.5 text-xs"
            >
              <div className="font-mono text-cyan-300 font-semibold text-[11px] mb-1.5 leading-normal">
                {ref.citation}
              </div>
              <div className="text-slate-400 leading-relaxed">
                <strong className="text-slate-200">Impact on Stack:</strong> {ref.keyContribution}
              </div>
            </div>
          ))}
        </div>

        {/* Section 8.4.1 Stack Defense Note */}
        <div className="mt-4 p-4 rounded-lg bg-slate-950/90 border border-slate-800 text-xs text-slate-300 leading-relaxed flex items-start gap-3">
          <FileText className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-100">Technical Stack Defense (Section 8.4.1):</strong> Baseline parity with Heller et al. (2012) requires canonical Internet2 (11 nodes) and AT&amp;T MPLS (21 nodes) benchmark backbones. For computational factorial scaling, seeded Barabási-Albert (power-law) and Waxman (geographic) synthetic models are evaluated across 60 scenario blocks with fixed random seeds for deterministic reproducibility.
          </div>
        </div>
      </div>
    </div>
  );
};
