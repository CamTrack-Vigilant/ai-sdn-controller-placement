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

- Key capability demonstrated:
- Main limitation acknowledged by authors:
- Data regime (size, quality, realism):
- Evaluation setting (controlled, synthetic, real-world):

## 3) Categorized SotA

### Technological SotA
- Best algorithms/architectures:

### Methodological SotA
- Training/validation method:
- Baselines compared against:

### Functional SotA
- What the system can do today:
- What it still cannot do reliably:

## 4) SotA vs Gap Test

- SotA statement:
- Gap statement:
- Why this gap matters for SDN controller placement research:

## 5) Your Notes

- Reusable ideas:
- Risks/bias concerns:
- Follow-up papers to read next:
