import React from 'react';
import { RESEARCH_HYPOTHESES, LITERATURE_REFERENCES } from '../data/benchmarkDatasets';
import { UnizuluOfficialSeal } from './UnizuluLogo';
import { UnizuluWaveSvgBackground } from './UnizuluOfficialWave';

const HONOURS_MILESTONES = [
  {
    milestone: 'Working Title & Proposal Summary Registration',
    date: '09 March 2026',
    deliverable: 'Registered with UNIZULU Dept. of Computer Science',
    status: '● Completed',
  },
  {
    milestone: 'Section 8.4.4 PyTorch AP-DQN Pilot & Factorial Run',
    date: '10 April 2026',
    deliverable: '50-episode Internet2 pilot validated at 0.0226s/episode',
    status: '● Completed',
  },
  {
    milestone: 'Proposal Ethics Protocol Package to Supervisors',
    date: '17 April 2026',
    deliverable: 'Submitted to Prof. P. Mudali & Dr. S. Zwane',
    status: '● Completed',
  },
  {
    milestone: 'Formal Honours Proposal Presentation',
    date: '18–25 May 2026',
    deliverable: 'Faculty of Science, Agriculture & Engineering Defense',
    status: '● Completed',
  },
  {
    milestone: 'Second Progress & Mock Exam Defense Rehearsal',
    date: '28 September 2026',
    deliverable: 'Multi-Objective Pareto Ledger & Statistical Verification',
    status: '● Completed',
  },
  {
    milestone: 'Final Oral Defense & Prototype Demonstration Window',
    date: '04–06 November 2026',
    deliverable: 'Interactive UNIZULU SDN Benchmarking Workbench & Dissertation',
    status: '● Active Window',
  },
];

export const HypothesisDashboard: React.FC = () => {
  return (
    <div className="space-y-8">
      {/* Official University of Zululand Proposal Stage Plan for R&D Cover Card */}
      <section className="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-xs">
        <div className="relative bg-[#00468B] text-white p-6 sm:p-10 overflow-hidden">
          <div className="absolute inset-0 pointer-events-none">
            <UnizuluWaveSvgBackground className="w-full h-full" />
          </div>

          <div className="hidden md:flex absolute top-4 right-6 z-20 flex-col items-center">
            <UnizuluOfficialSeal size="md" />
          </div>

          <div className="relative z-10 max-w-3xl pb-8">
            <div className="flex flex-wrap items-center gap-2 text-xs text-[#FFF200] font-semibold mb-2">
              <span>Proposal Stage Plan for R and D</span>
              <span aria-hidden="true">·</span>
              <span>Workshop Part 2</span>
              <span aria-hidden="true">·</span>
              <span>KwaDlangezwa Campus</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              Evidence-Based Multi-Objective Evaluation of AI and Heuristic Controller Placement for Multi-Site Software Defined Networks
            </h2>
            <div className="flex flex-wrap items-center gap-2 text-xs text-white/95 mt-3 font-mono tabular-nums">
              <span>Candidate: Thabang Nhlokoma Buthelezi</span>
              <span aria-hidden="true">·</span>
              <span>Student No: 230011908</span>
              <span aria-hidden="true">·</span>
              <span>Degree: BSc Honours (Computer Science)</span>
            </div>
            <div className="flex flex-wrap items-center gap-2 text-xs text-blue-100 mt-1">
              <span>Supervisor: Prof. Pragasen Mudali</span>
              <span aria-hidden="true">·</span>
              <span>Co-Supervisor: Dr. Skhumbuzo Zwane</span>
              <span aria-hidden="true">·</span>
              <span className="italic text-[#FFF200] font-medium">
                Motto: Diligentia Cresco (“Through diligence, I grow”)
              </span>
            </div>
          </div>
        </div>

        {/* Section 8.1 - 8.4.1 Methodological Summary Grid */}
        <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6 text-xs bg-white">
          <div className="p-4 bg-[#F8FAFC] border border-slate-200 rounded-md">
            <div className="font-bold text-[#0061AF] mb-1">
              01. Positivist &amp; Deductive Paradigm (Sec. 8.1–8.2)
            </div>
            <p className="text-slate-600 leading-relaxed">
              Grounded in quantitative post-positivist inquiry. Controller placement strategies generate observable, deterministic metrics (propagation delay in ms, single-link fault reachability, and episode runtime cost) across seeded trials.
            </p>
          </div>

          <div className="p-4 bg-[#F8FAFC] border border-slate-200 rounded-md">
            <div className="font-bold text-[#84383E] mb-1">
              02. Technical Stack Defense (Sec. 8.4.1)
            </div>
            <p className="text-slate-600 leading-relaxed">
              Baseline parity with Heller et al. (2012) enforces Internet2 (11 nodes) and AT&amp;T MPLS (21 nodes) primary backbones alongside Barabási-Albert and Waxman synthetic factorial scaling, paired with Farahi et al. (2026) AP-DQN hyperparameters.
            </p>
          </div>

          <div className="p-4 bg-[#F8FAFC] border border-slate-200 rounded-md">
            <div className="font-bold text-slate-900 mb-1">
              03. Pilot Computational Feasibility (Sec. 11.2)
            </div>
            <p className="text-slate-600 leading-relaxed">
              Validated 50-episode AP-DQN pilot run on Internet2 completed 500 environment steps in 1.13 seconds (<span className="font-mono">0.0226s/episode</span>), confirming full factorial tractability within the UNIZULU Honours timeline.
            </p>
          </div>
        </div>
      </section>

      {/* Deductive Research Hypotheses & Empirical Verdicts */}
      <section className="bg-white border border-slate-200 rounded-lg p-6">
        <div className="pb-4 mb-5 border-b border-slate-200">
          <div className="text-xs text-[#0061AF] font-semibold mb-1">
            Section 8.5.1 Golden Thread Mapping: Research Questions to Inferential Analysis
          </div>
          <h3 className="font-bold text-slate-900 text-lg tracking-tight">
            Deductive Research Hypotheses &amp; Empirical Findings
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {RESEARCH_HYPOTHESES.map((h) => (
            <div
              key={h.id}
              className="bg-[#FAFBFD] border border-slate-200 rounded-md p-5 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between text-xs pb-3 mb-3 border-b border-slate-200">
                  <span className="font-mono font-bold text-[#0061AF]">
                    Hypothesis {h.id}
                  </span>
                  <span className="font-mono font-semibold text-emerald-700">
                    ● {h.verdict}
                  </span>
                </div>
                <h4 className="font-bold text-slate-900 text-sm mb-2">{h.title}</h4>
                <p className="text-xs text-slate-600 leading-relaxed mb-4">
                  {h.statement}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-200 text-xs">
                <div className="font-semibold text-slate-800 mb-1">Empirical Evidence:</div>
                <p className="text-slate-600 leading-relaxed mb-2.5">
                  {h.evidence}
                </p>
                <div className="font-mono text-[11px] text-[#84383E] font-medium">
                  Statistical Note: {h.significance}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* UNIZULU Honours Programme Milestone Schedule */}
      <section className="bg-white border border-slate-200 rounded-lg p-6">
        <div className="pb-4 mb-5 border-b border-slate-200">
          <div className="text-xs text-[#84383E] font-semibold mb-1">
            Section 11.3 Programme Alignment &amp; Execution Audit
          </div>
          <h3 className="font-bold text-slate-900 text-lg tracking-tight">
            UNIZULU BSc Honours (Computer Science) 2026 Milestone Ledger
          </h3>
        </div>

        <div className="overflow-x-auto border border-slate-200 rounded-md">
          <table className="w-full text-left text-xs text-slate-800">
            <thead className="bg-[#F8FAFC] text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Programme Milestone</th>
                <th className="py-3 px-4">Target Date</th>
                <th className="py-3 px-4">Verified Project Artifact</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {HONOURS_MILESTONES.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="py-2.5 px-4 font-semibold text-slate-900">
                    {item.milestone}
                  </td>
                  <td className="py-2.5 px-4 font-mono tabular-nums text-slate-600 whitespace-nowrap">
                    {item.date}
                  </td>
                  <td className="py-2.5 px-4 text-slate-600">{item.deliverable}</td>
                  <td className="py-2.5 px-4 font-mono text-xs font-semibold text-[#0061AF] whitespace-nowrap">
                    {item.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Authoritative References & Bibliography */}
      <section className="bg-white border border-slate-200 rounded-lg p-6">
        <div className="pb-4 mb-5 border-b border-slate-200">
          <div className="text-xs text-[#0061AF] font-semibold mb-1">
            Section 15 Authoritative Bibliography (Harvard &amp; IEEE Cross-Referenced)
          </div>
          <h3 className="font-bold text-slate-900 text-lg tracking-tight">
            Foundational Literature &amp; Methodological Anchors
          </h3>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {LITERATURE_REFERENCES.map((ref) => (
            <div
              key={ref.id}
              className="bg-[#F8FAFC] border border-slate-200 rounded-md p-4 text-xs"
            >
              <div className="font-mono text-[#004987] font-semibold text-[11px] mb-1.5 leading-normal">
                {ref.citation}
              </div>
              <div className="text-slate-600 leading-relaxed">
                <strong className="text-slate-900">Methodological Role:</strong>{' '}
                {ref.keyContribution}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
