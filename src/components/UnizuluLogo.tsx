import React, { useState } from 'react';

interface UnizuluCrestProps {
  className?: string;
}

/**
 * Vector heraldic shield & African Fish Eagle crest of the University of Zululand
 * Arms: Gyronny of twelve argent and azure, at nombril point, on a bezant (#FFF200), a pall sable (#231F20).
 * Crest: African Fish Eagle displayed, proper (#844349 burgundy & argent).
 * Motto: DILIGENTIA CRESCO ("Through diligence, I grow").
 */
export const UnizuluCrestSvg: React.FC<UnizuluCrestProps> = ({ className = 'w-9 h-9' }) => (
  <svg
    viewBox="0 0 120 135"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
    aria-label="University of Zululand Heraldic Crest"
  >
    {/* Mantling (Blue & Silver/White) */}
    <path
      d="M28 45 C14 38, 12 58, 24 64 C14 72, 18 90, 32 88"
      stroke="#0061AF"
      strokeWidth="7"
      strokeLinecap="round"
    />
    <path
      d="M92 45 C106 38, 108 58, 96 64 C106 72, 102 90, 88 88"
      stroke="#0061AF"
      strokeWidth="7"
      strokeLinecap="round"
    />
    <path
      d="M31 49 C20 44, 19 57, 27 62"
      stroke="#CBD5E1"
      strokeWidth="3.5"
      strokeLinecap="round"
    />
    <path
      d="M89 49 C100 44, 101 57, 93 62"
      stroke="#CBD5E1"
      strokeWidth="3.5"
      strokeLinecap="round"
    />

    {/* African Fish Eagle Crest */}
    <path
      d="M32 12 L48 22 L54 14 L60 10 L66 14 L72 22 L88 12 L82 28 L68 32 L60 36 L52 32 L38 28 Z"
      fill="#64748B"
      stroke="#231F20"
      strokeWidth="1.5"
    />
    <path
      d="M48 18 L55 34 L65 34 L72 18 L64 22 L56 22 Z"
      fill="#844349"
    />
    <circle cx="60" cy="14" r="5" fill="#FFFFFF" stroke="#231F20" strokeWidth="1.2" />
    {/* Torse / Wreath (Argent and Azure) */}
    <rect x="44" y="34" width="32" height="5" rx="2.5" fill="#0061AF" stroke="#231F20" strokeWidth="1.2" />
    {/* Helmet */}
    <path d="M48 39 H72 L69 49 H51 Z" fill="#231F20" stroke="#ED1C24" strokeWidth="1.2" />

    {/* Heraldic Shield Base (Azure #0061AF) */}
    <path
      d="M32 49 H88 V79 C88 100 60 113 60 113 C60 113 32 100 32 79 Z"
      fill="#0061AF"
      stroke="#231F20"
      strokeWidth="2"
    />

    {/* Gyronny of Twelve Rays (Argent #FFFFFF radiating from nombril point 60,84) */}
    <polygon points="60,84 44,49 55,49" fill="#FFFFFF" />
    <polygon points="60,84 65,49 76,49" fill="#FFFFFF" />
    <polygon points="60,84 32,62 32,75" fill="#FFFFFF" />
    <polygon points="60,84 88,62 88,75" fill="#FFFFFF" />
    <polygon points="60,84 35,92 44,102" fill="#FFFFFF" />
    <polygon points="60,84 85,92 76,102" fill="#FFFFFF" />

    {/* Shield Border */}
    <path
      d="M32 49 H88 V79 C88 100 60 113 60 113 C60 113 32 100 32 79 Z"
      fill="none"
      stroke="#004987"
      strokeWidth="2.2"
    />

    {/* Golden Bezant at Nombril Point (#FFF200) */}
    <circle
      cx="60"
      cy="84"
      r="13.5"
      fill="#FFF200"
      stroke="#231F20"
      strokeWidth="2"
    />

    {/* Sable Pall (Y-shape inside Bezant) */}
    <path
      d="M50 76 L60 84 L70 76 M60 84 V97"
      stroke="#231F20"
      strokeWidth="4"
      strokeLinecap="butt"
      fill="none"
    />

    {/* Motto Scroll: DILIGENTIA CRESCO */}
    <path
      d="M26 112 Q60 128 94 112 L91 121 Q60 136 29 121 Z"
      fill="#0061AF"
      stroke="#004987"
      strokeWidth="1.2"
    />
  </svg>
);

interface UnizuluOfficialSealProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

/**
 * Displays the authentic official University of Zululand logo extracted from the proposal PDF,
 * with resilient SVG fallback.
 */
export const UnizuluOfficialSeal: React.FC<UnizuluOfficialSealProps> = ({
  size = 'md',
  className = '',
}) => {
  const [imgError, setImgError] = useState(false);

  const sizeClasses = {
    sm: 'h-14 w-auto',
    md: 'h-24 w-auto',
    lg: 'h-32 w-auto',
  }[size];

  if (imgError) {
    return (
      <div className={`inline-flex flex-col items-center bg-white p-2 rounded border border-slate-200 ${className}`}>
        <UnizuluCrestSvg className="w-14 h-16" />
        <span className="text-[10px] font-bold tracking-wider text-[#231F20] mt-1">
          UNIVERSITY OF ZULULAND
        </span>
        <span className="text-[8px] font-semibold italic text-[#0061AF]">
          A NODE FOR AFRICAN THOUGHT
        </span>
      </div>
    );
  }

  return (
    <img
      src="/unizulu-logo.jpg"
      alt="University of Zululand Official Coat of Arms — A Node for African Thought"
      referrerPolicy="no-referrer"
      onError={() => setImgError(true)}
      className={`${sizeClasses} object-contain select-none ${className}`}
    />
  );
};
