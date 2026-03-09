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
