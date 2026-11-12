import React from 'react';
import { UnizuluOfficialSeal } from './UnizuluLogo';

interface UnizuluWaveBackgroundProps {
  className?: string;
}

/**
 * Exact vector recreation of the official University of Zululand corporate presentation & banner wave design
 * matching the official school template (/assets/aistudio/WhatsApp_Image_2026-11-08_at_22.09.23_6a50b93d.jpeg):
 * - Primary field: UNIZULU Royal-to-Navy Blue gradient (#0055A6 -> #00376B)
 * - Top-right: Burgundy wedge (#84383E), white sweeping ribbon, and white curved lobe for the UNIZULU Coat of Arms
 * - Bottom-left to bottom-right: White flowing S-wave ribbon, Black taper (#111111), Vibrant Yellow wedge (#FFF200),
 *   lower Royal Blue arch (#0055A6), and bottom-right Burgundy corner (#84383E).
 */
export const UnizuluWaveSvgBackground: React.FC<UnizuluWaveBackgroundProps> = ({
  className = 'w-full h-full',
}) => (
  <svg
    viewBox="0 0 1600 900"
    preserveAspectRatio="none"
    className={className}
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <defs>
      <linearGradient id="unizuluMainBlue" x1="0%" y1="0%" x2="100%" y2="20%">
        <stop offset="0%" stopColor="#0057A8" />
        <stop offset="55%" stopColor="#00468B" />
        <stop offset="100%" stopColor="#00356B" />
      </linearGradient>
      <linearGradient id="unizuluLowerBlue" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stopColor="#0058AA" />
        <stop offset="100%" stopColor="#004488" />
      </linearGradient>
    </defs>

    {/* 1. Primary Royal-to-Navy Blue Field */}
    <rect width="1600" height="900" fill="url(#unizuluMainBlue)" />

    {/* 2. Top-Right Burgundy Wedge (#84383E) */}
    <path
      d="M 960 0 L 1265 0 C 1270 115, 1300 215, 1345 275 C 1225 145, 1105 35, 960 0 Z"
      fill="#84383E"
    />

    {/* 3. Top-Right White Curved Ribbon & Official Logo Lobe */}
    <path
      d="M 905 0 L 975 0 C 1105 40, 1225 150, 1335 268 C 1278 190, 1252 105, 1250 0 L 1600 0 L 1600 325 C 1510 420, 1375 415, 1270 300 C 1140 160, 1040 42, 905 0 Z"
      fill="#FFFFFF"
    />

    {/* 4. Bottom-Right Burgundy Wedge (#84383E) */}
    <path
      d="M 980 830 C 1190 865, 1390 795, 1600 665 L 1600 900 L 1245 900 Z"
      fill="#84383E"
    />

    {/* 5. Bottom-Left Yellow/Gold Wedge (#FFF200) */}
    <path
      d="M 0 345 C 95 455, 310 565, 625 668 C 365 595, 65 585, 0 805 Z"
      fill="#FFF200"
    />

    {/* 6. Left Black Accent Taper (#111111) */}
    <path
      d="M 0 302 C 65 390, 175 462, 310 520 C 165 468, 58 408, 0 352 Z"
      fill="#111111"
    />

    {/* 7. Main Flowing White S-Wave Ribbon */}
    <path
      d="M 0 250 C 90 400, 340 520, 860 695 C 1195 808, 1390 760, 1600 622 L 1600 672 C 1385 815, 1180 868, 845 752 C 335 575, 85 450, 0 305 Z"
      fill="#FFFFFF"
    />

    {/* 8. Bottom-Left Arching Royal Blue Wave */}
    <path
      d="M 0 900 L 0 800 C 45 595, 345 580, 665 680 C 895 752, 1085 832, 1275 900 Z"
      fill="url(#unizuluLowerBlue)"
    />
  </svg>
);

interface UnizuluHeroBannerProps {
  activeTabLabel: string;
  onOpenSlideDeck?: () => void;
}

/**
 * Official University of Zululand Hero Header using the exact school wave design
 * and housing the official UNIZULU Coat of Arms in the top-right white lobe.
 */
export const UnizuluHeroBanner: React.FC<UnizuluHeroBannerProps> = ({
  activeTabLabel,
  onOpenSlideDeck,
}) => {
  return (
    <section
      aria-label="University of Zululand Official Research Header"
      className="relative w-full overflow-hidden bg-[#00468B] text-white border-b border-slate-300 shadow-sm"
    >
      {/* Vector recreation of the official UNIZULU wave design */}
      <div className="absolute inset-0 pointer-events-none">
        <UnizuluWaveSvgBackground className="w-full h-full object-cover" />
      </div>

      {/* Top-Right Official Coat of Arms positioned inside the white curved lobe */}
      <div className="hidden lg:flex absolute top-3 right-8 z-20 flex-col items-center justify-center pointer-events-none">
        <UnizuluOfficialSeal size="md" className="drop-shadow-xs" />
      </div>

      {/* Foreground Academic Content */}
      <div className="relative z-10 max-w-[1380px] mx-auto px-6 pt-7 pb-14 lg:py-10">
        <div className="max-w-3xl">
          {/* Mobile / Tablet Logo fallback */}
          <div className="lg:hidden inline-flex items-center bg-white rounded-lg p-2 mb-4 shadow-xs">
            <UnizuluOfficialSeal size="sm" />
          </div>

          <div className="flex flex-wrap items-center gap-2 text-xs font-medium text-[#FFF200] mb-2">
            <span>UNIVERSITY OF ZULULAND</span>
            <span aria-hidden="true">·</span>
            <span>FACULTY OF SCIENCE, AGRICULTURE &amp; ENGINEERING</span>
            <span aria-hidden="true">·</span>
            <span>DEPT. OF COMPUTER SCIENCE</span>
          </div>

          <h1
            className="text-2xl sm:text-3xl lg:text-[34px] font-bold text-white tracking-tight leading-[1.18]"
            style={{ textWrap: 'balance' }}
          >
            Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site SDN
          </h1>

          <p className="text-sm sm:text-base text-blue-100 mt-2.5 max-w-2xl leading-relaxed">
            Proposal Stage Plan for R&amp;D &amp; Experimental Evaluation Framework · Balancing Control-Plane Latency, N-1 Survivability, and Computational Cost
          </p>

          {/* Candidate & Supervisor Metadata — Clean Unboxed Typography */}
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-white/95 mt-4 pt-3 border-t border-white/20 font-mono tabular-nums">
            <span>
              Candidate: <strong>Thabang Nhlokoma Buthelezi</strong>
            </span>
            <span aria-hidden="true">·</span>
            <span>Student No: 230011908</span>
            <span aria-hidden="true">·</span>
            <span>BSc Honours (Computer Science)</span>
            <span aria-hidden="true">·</span>
            <span>
              Supervisors: <strong>Prof. P. Mudali</strong> &amp; <strong>Dr. S. Zwane</strong>
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-4 mt-4 text-xs">
            <span className="text-blue-100 font-medium">
              Active Module: <strong className="text-[#FFF200]">{activeTabLabel}</strong>
            </span>
            {onOpenSlideDeck && (
              <>
                <span aria-hidden="true" className="text-white/40">
                  |
                </span>
                <button
                  onClick={onOpenSlideDeck}
                  className="underline decoration-[#FFF200] underline-offset-4 font-semibold text-white hover:text-[#FFF200] transition-colors cursor-pointer"
                >
                  Open Official UNIZULU R&amp;D Presentation Slide Deck →
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};
