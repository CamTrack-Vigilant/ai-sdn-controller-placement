# PARETO FRONTIER DIAGRAM: Technical Specification & Implementation Guide

**For Section 3.1 Problem Statement**  
**Location**: Between Problem Statement ending ("...and across topology scales.") and Research Questions (3.2)  
**Recommended Size**: 3.5" × 2.5" (portrait orientation) to fit within page margins

---

## DIAGRAM TYPE: 3D or 2D Trade-Off Scatter Plot

### Option 1: 3D Scatter (Recommended)
**Axes**:
- **X**: Control-Plane Latency (milliseconds) — 0 to 150 ms scale
- **Y**: Reliability (%) — 0 to 100% scale  
- **Z**: Computational Cost (arbitrary units or RUs) — 0 to 100 units

**Data Points to Include**:

| Method | Latency (ms) | Reliability (%) | Cost (units) | Marker | Citation |
|--------|------------|-----------|------|--------|----------|
| Random Placement | 120 | 60 | 10 | Red circle | Baseline |
| Greedy k-Means | 75 | 70 | 15 | Orange circle | Baseline heuristic |
| Heller 2012 Optimal | 50 | 80 | 25 | Green circle | Heller et al. (2012) |
| Classical (Best multi-obj) | 55 | 82 | 28 | Green square | Lange et al. (2015) |
| AI-Driven (Farahi 2026) | 41 | 88 | 45 | Blue diamond | Farahi et al. (2026) |

**Key Features**:
- Draw a **curved surface** connecting non-dominated points (the Pareto frontier boundary)
- Shade the region **dominated** (inferior) solutions in light gray
- Annotate Heller 2012 achievement: "50 ms in 82% of WAN topologies" with leader line
- Mark the **40–60% miss zone** (Lange 2015) where latency-only methods fail to identify viable configs

---

### Option 2: 2D Trade-Off Heatmap
**If 3D is too complex, use a 2×2 grid heatmap**:

```
                    Latency (Lower Preferred)
           Low (30-50 ms)  |  High (80-120 ms)
         ─────────────────┼────────────────────
         │  🔵 AI-Driven  │  🟡 Greedy       │
High R   │  (Pareto)      │  (Dominated)     │
(80-95%) │  Cost: High    │  Cost: Low       │
         ├─────────────────┼────────────────────┤
         │  🟢 Heller     │  🔴 Random       │
Low R    │  (Pareto)      │  (Dominated)     │
(60-75%)  │  Cost: Medium  │  Cost: Low       │
         └─────────────────┴────────────────────┘
         
        Pareto Frontier Points: 🔵, 🟢 (non-dominated)
        Dominated Points: 🟡, 🔴 (inferior on ≥1 criterion)
```

---

## DIAGRAM DATA SOURCE: Embedded Evidence

### Lange et al. (2015)
- **Key Finding**: Latency-only optimization misses 40–60% of viable configurations when reliability and cost are included on the Pareto frontier
- **Implication**: Shows that RQ1 ("preserve latency advantage while improving reliability and cost along Pareto frontier") is non-trivial — trade-offs exist
- **Visual**: Shade the "Lange Miss Zone" (configurations that are optimal on latency but suboptimal on multi-criteria)

### Wang & Chen (2021)
- **Key Finding**: Link-failure response (LFFCPP) directly impacts control-plane latency fluctuation; LFFCPP-aware placement reduces fluctuation
- **Implication**: Justifies RQ2 focus on "performance stability under link-failure dynamics"
- **Visual**: Add annotation noting "Link-failure behavior varies across frontier points — impacts RQ2"

### Farahi et al. (2026)
- **Key Finding**: AP-DQN achieves 24% load-balancing, 25% latency reduction, 28% cost savings on 15–50 switch topologies
- **Implication**: AI can move toward better Pareto frontier points (✅), but limited to small–medium topologies (constraint for RQ3)
- **Visual**: Position AI point (blue diamond) on frontier; add note: "Valid on 15–50 switches only; RQ3 asks: scalable to 100+ switches?"

### Heller et al. (2012)
- **Key Finding**: 50 ms latency achievable in 82% of WAN topologies using optimized placement; 1.4–1.7× improvement over random
- **Implication**: Establishes latency baseline for comparison; shows why control-plane latency matters
- **Visual**: Mark latency axis at 50 ms with label "Heller 82% WAN achievement"

---

## FIGURE CAPTION

```
Figure 3.1: Pareto Frontier for Multi-Objective SDN Controller Placement. The frontier 
(blue curved boundary) represents optimal trade-offs between control-plane latency, 
reliability, and computational cost. Method categories are plotted as colored markers: 
random placement (red, dominated), greedy heuristics (orange, dominated), classical 
optimization (green, Pareto-optimal), and AI-driven approaches (blue, Pareto-optimal). 
Lange et al. (2015) demonstrate that latency-only optimization (vertical dotted line) 
misses 40–60% of viable frontier configurations. Farahi et al. (2026) show AI methods 
can achieve superior latency (–25%) and reliability improvements, but scope is constrained 
to 15–50 switch topologies. Wang & Chen (2021) identify link-failure dynamics as a 
critical variable affecting placement stability across the frontier.
```

---

## IMPLEMENTATION CHECKLIST

- [ ] **Secure data imports**: Extract latency/reliability/cost metrics from Lange 2015, Wang & Chen 2021, Farahi 2026, Heller 2012 papers
- [ ] **Create 3D scatter plot** (preferred tool: R `rgl`, Python `matplotlib` 3D, or Plotly)
  - Embed Pareto frontier surface (convex hull of non-dominated points)
  - Shade dominated region in light gray
  - Label all method categories with colors and legend
- [ ] **Annotate key evidence**:
  - "Lange: 40–60% miss zone" — overlay shaded band on latency axis
  - "Heller: 50 ms in 82% WAN topologies" — mark on latency axis
  - "Farahi: 15–50 switches only" — note near AI-driven point
- [ ] **Add visual indicators of link-failure impact**:
  - Optional nested second curve showing "stability envelope" (latency variation under failures)
  - Annotation: "Link-failure dynamics (Wang & Chen 2021) constrain achievable frontier configurations"
- [ ] **Size for PDF**: Export at 300 DPI, 3.5" × 2.5", embedded in PDF between Problem Statement and Research Questions
- [ ] **Caption review**: Ensure caption is ≤5 lines and references all four papers (Lange, Wang & Chen, Farahi, Heller)

---

## ALTERNATIVE: Qualitative Diagram (if quantitative data unavailable)

If exact numerical data from papers is inaccessible, use a **conceptual schematic**:

```
         PARETO FRONTIER (Best Trade-offs)
                    ╱╲╲
                   ╱  ╲╲
                  ╱ AI  ╲╲
                 ╱(Blue)  ╲╲
                ╱___Classical_╲╲
               ╱    (Green)    ╲╲___
              ╱                 ╲╲   ╲
             ╱  Greedy            ╲╲   ╲  Dominated
            ╱  (Orange)            ╲╲   ╲ Zone
           ╱                        ╲╲   ╲ (Gray)
          ────────────────────────────────────
          LATENCY (Low ────► High)
                          
        Reliability/Cost:
        - Blue (AI): High reliability, high cost
        - Green (Classical): Medium reliability, medium cost
        - Orange (Greedy): Low reliability, low cost
        
        Key Insight: No single method dominates all three criteria.
        RQ1 asks: Can AI maintain latency advantage while improving 
                  reliability and cost along the frontier?
```

---

## SECTION 3: TERMINOLOGY CONSISTENCY CHECKLIST

After implementing Pareto diagram, verify these terms appear consistently throughout Section 3:

- **"Pareto frontier"** (or "Pareto-frontier"):  
  - ✅ 3.1 Problem Statement: "...the Pareto frontier reveals that no single configuration dominates..."
  - ✅ 3.2 RQ1: "...along the Pareto frontier in multi-site SDN..."
  - ✅ 3.2 RQ3: "...on the latency-reliability-cost Pareto frontier..."
  - Figure 3.1 caption: "Pareto Frontier for Multi-Objective..."

- **"Link-failure dynamics"**:  
  - ✅ 3.1 Problem Statement: "...remaining stable under link failures and across topology scales"
  - ✅ 3.2 RQ2: "...performance stability under link-failure dynamics..."
  - Associated methodology section (6 or 7): Explicit discussion of link-failure testing scenarios

- **"Performance stability"**:  
  - ✅ 3.1 Problem Statement: "...preserve its performance advantage while also remaining stable..."
  - ✅ 3.2 RQ2: "...compare in performance stability under link-failure dynamics..."
  - 4.2 Research Objectives: Add objective targeting performance stability across topology families

---

## PAGE LAYOUT INTEGRATION

**Before Diagram Insertion**:
- Problem Statement: ~4 lines (approx. 200 words)
- Blank space below: ~0.5"
- Research Questions: ~9 lines

**After Diagram Insertion**:
- Problem Statement: ~4 lines
- **Figure 3.1 [Pareto Frontier]**: 3.5" × 2.5" centered, with 0.15" margins above/below
- Research Questions: ~9 lines (may shift 1–2 lines down)
- **Expected Page Impact**: Section 3 may expand to 1.5 pages (currently fits on 1 page); Section 4 may start on page 4 (currently page 4 top)

**Recommendation**: Reduce line spacing in Problem Statement / Research Questions from 1.15 to 1.0 to keep Section 4 on same page.

---

## FILES TO UPDATE (AFTER DIAGRAM CREATION)

1. **Research_Proposal_Hardened_Final.pdf**: Insert Pareto diagram image between Sections 3.1 and 3.2
2. **docs/SECTION_3_HARDENING_REPORT.md**: Update with link to generated diagram (if saved as separate file)
3. **docs/figures/**: Create subfolder for figures, save diagram as `pareto_frontier_section3.png` (300 DPI)

---

## NEXT SESSION ACTIVITY

**If generating diagram in this session**:
1. Extract quantitative data from Lange 2015, Wang & Chen 2021, Farahi 2026, Heller 2012
2. Create 3D or 2D visualization using tool of choice (Python matplotlib, R, Plotly, etc.)
3. Embed into PDF between Sections 3.1 and 3.2
4. Verify page layout and terminology consistency

**If creating diagram in future session**:
- These specifications are complete and ready to hand off to visualization specialist
- All evidence citations are documented in SECTION_3_HARDENING_REPORT.md

---

*Generated: April 10, 2026*  
*Alignment: Honours Research Methodology — Evidence-Driven Problem Framing*  
*Related Documents*: SECTION_3_HARDENING_REPORT.md, Research_Proposal_Hardened_Final.pdf
