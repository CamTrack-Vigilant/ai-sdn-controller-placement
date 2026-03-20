# Paper Extraction Template

## Basic Metadata

- Paper file: SDN-based Solutions.pdf
- Title: SDN-based Solutions for Improving Network Performance
- Authors: Raid Boudi
- Venue: Doctoral Thesis, University of Mila (Faculty of Mathematics and Computer Sciences)
- Year: 2026 (defended January 24, 2026; academic year 2025-2026)
- Domain: SDN

## 1) SotA Indicators

- Gold-standard models mentioned: WBC-CPP, GWO-WBC-CPP, PSO-HSL (plus baselines such as HC-BC and Louvain-BC in comparative analysis).
- Best metric reported: Multi-metric improvement over baselines across average switch-controller latency, controller-controller latency, and switch-controller flow rate.
- Metric value: Improvement table reports up to 19.89% (Avg. SC latency), up to 33.16% (SC flow rate), and up to 55.01% (Avg. CC latency) over compared baselines/scenarios.
- Efficiency claim (if any): GWO-WBC-CPP(50%) achieves near-equivalent latency/flow quality to GWO-WBC-CPP(100%) while reducing optimization time (execution-time advantage from search-space reduction).
- Claimed turning-point year: Not explicitly stated as a single turning-point year.
- Evidence quote (copy exact sentence + section):
	- Abstract: "The results show notable performance gains in terms of latency, load balancing, reliability, and overall network efficiency when compared to conventional CPP and baseline SDN placement methods."
	- Chapter 6 (improvement summary table text extraction): "Avg. SC Latency (ms) 17.15% 19.89% 15.75% 18.54%", "SC Flow Rate (flow/ms) 26.63% 33.16% 23.51% 29.88%", "Avg. CC Latency (ms) 33.63% 32.27% 55.01% 54.08%".

## 2) Synthesis Inputs

- Key capability demonstrated: Provides a broad empirical comparison of multiple CPP families and reports improvements on latency, flow rate, and controller-controller delay.
- Main limitation acknowledged by authors: As a thesis-level consolidated study, reproducibility details and cross-lab replication evidence may be uneven across chapters.
- Data regime (size, quality, realism): Multi-scenario simulation data with aggregate improvement tables across compared approaches.
- Evaluation setting (controlled, synthetic, real-world): Controlled simulation and comparative experimental analysis.

## 3) Categorized SotA

### Technological SotA
- Best algorithms/architectures: WBC-CPP, GWO-WBC-CPP, and PSO-HSL with comparative reference to additional baseline families.

### Methodological SotA
- Training/validation method: Comparative multi-metric evaluation over latency, load balancing, reliability, and flow-related outcomes.
- Baselines compared against: Conventional CPP and baseline SDN placement methods, including HC-BC and Louvain-BC references.

### Functional SotA
- What the system can do today: Show that targeted optimization can improve several operational metrics at once in controlled settings.
- What it still cannot do reliably: Provide a universally transferable ranking across topology families and strict compute budgets.

## 4) SotA vs Gap Test

- SotA statement: Multi-algorithm CPP studies can reveal strong practical improvements and useful trade-off patterns.
- Gap statement: Standardized, reproducible efficiency-frontier comparisons across methods are still limited.
- Why this gap matters for SDN controller placement research: Thesis-grade evidence needs not only improvement percentages but also transparent reproducibility and scenario-conditioned interpretation.

## 5) Your Notes

- Reusable ideas: Improvement-summary table format and search-space reduction variants for runtime-sensitive experimentation.
- Risks/bias concerns: Potential chapter-level heterogeneity in experiment assumptions and parameter fairness across compared methods.
- Follow-up papers to read next: symmetry-15-01520-v2.pdf; 1-s2.0-S2590123026006717-main.pdf; peerj-cs-1698.pdf.
