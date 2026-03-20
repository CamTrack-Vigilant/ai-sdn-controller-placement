# Paper Extraction Template

## Basic Metadata

- Paper file: computers-11-00111.pdf
- Title: Multi-Controllers Placement Optimization in SDN by the Hybrid HSA-PSO Algorithm
- Authors: Neamah S. Radam; Sufyan T. Faraj Al-Janabi; Khalid Sh. Jasim
- Venue: Computers (MDPI)
- Year: 2022
- Domain: SDN Controller Placement (multi-controller)

## 1) SotA Indicators

- Gold-standard models mentioned: Hybrid HSA-PSO (MC-SDN), with SA-FFCCPP and GSOCCPP as comparison baselines.
- Best metric reported: Propagation latency, average delay, reliability, throughput, and fitness value.
- Metric value: Propagation latency 11-20 ms (vs 22-40 ms and 27-45 ms baselines); reliability 0.88 +/- 0.1 (vs 0.79 +/- 0.4 and 0.75 +/- 0.5); throughput 197.1 +/- 0.1 (vs 165.7 +/- 0.2 and 150.2 +/- 0.3).
- Efficiency claim (if any): Reduced average delay and better optimization fitness/convergence for controller placement (fitness 22.5 vs 18.2 and 16.4 baselines).
- Claimed turning-point year: Not explicitly stated as a field-wide turning-point year.
- Evidence quote (copy exact sentence + section):
	- Conclusions and Future Work: "A hybrid metaheuristic algorithm is proposed in this research to deploy multiple controllers effectively, in order to reduce communication and propagation latency and improve throughput and reliability."
	- Results section (numerical analysis snippets): "The proposed MC-SDN method achieves low propagation latency (11 to 20 ms) when compared with SA-FFCCPP (22 to 40 ms) and GSOCCPP (27 to 45 ms) methods." and "Numerical analysis of reliability... MC-SDN 0.88 +/- 0.1".

## 2) Synthesis Inputs

- Key capability demonstrated: Demonstrates that a hybrid HSA-PSO search can improve latency, throughput, reliability, and fitness versus compared metaheuristics.
- Main limitation acknowledged by authors: Evidence is simulation-heavy and may not fully cover real-time operational variability or standardized reproducibility controls.
- Data regime (size, quality, realism): Controlled simulation scenarios with quantitative latency/reliability/throughput measurements.
- Evaluation setting (controlled, synthetic, real-world): Controlled synthetic evaluation with comparative baselines.

## 3) Categorized SotA

### Technological SotA
- Best algorithms/architectures: Hybrid HSA-PSO multi-controller placement optimizer (MC-SDN).

### Methodological SotA
- Training/validation method: Metaheuristic optimization over placement fitness with comparative numeric evaluation.
- Baselines compared against: SA-FFCCPP and GSOCCPP.

### Functional SotA
- What the system can do today: Improve placement quality on selected metrics in controlled experiments.
- What it still cannot do reliably: Guarantee consistent gains under broader topology diversity, dynamic workloads, and compute constraints.

## 4) SotA vs Gap Test

- SotA statement: Hybrid metaheuristics can be competitive for multi-controller optimization in static simulation settings.
- Gap statement: Evidence is still weak on reproducible cross-topology efficiency frontiers and seed-stability behavior.
- Why this gap matters for SDN controller placement research: Without robust cross-scenario validation, reported improvements may not transfer to operational decision-making.

## 5) Your Notes

- Reusable ideas: Multi-metric reporting format and fitness-based comparative benchmarking.
- Risks/bias concerns: Metaheuristic parameter sensitivity and possible premature convergence artifacts.
- Follow-up papers to read next: symmetry-15-01520-v2.pdf; 1-s2.0-S2590123026006717-main.pdf; 2377677.2377767.pdf.
