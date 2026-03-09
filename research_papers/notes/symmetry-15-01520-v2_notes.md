# Paper Extraction Template

## Basic Metadata

- Paper file: symmetry-15-01520-v2.pdf
- Title: A Multi-Controller Placement Strategy for Hierarchical Management of Software-Defined Networking
- Authors: Hui Xu; Xiaodi Chai; Huifen Liu
- Venue: Symmetry (MDPI)
- Year: 2023
- Domain: SDN Controller Placement (hierarchical multi-controller)

## 1) SotA Indicators

- Gold-standard models mentioned: MOIHHO (proposed multi-objective improved Harris Hawks Optimization), with NSGA-II and MOPSO as baseline competitors.
- Best metric reported: Integrated latency, reliability, load variance, and integrated placement overhead under large-scale real topologies.
- Metric value: Compared to MOPSO, MOIHHO reports about 8% reduction in worst switch-to-local-controller latency, about 10% increase in reliability, about 20% reduction in load variance, and about 10% reduction in combined placement overhead; compared to NSGA-II, worst latency about 20% lower, average latency about 5% lower, reliability about 7% higher, and overhead about 14% lower.
- Efficiency claim (if any): Better robustness/adaptability as topology size and link complexity increase, while maintaining load balancing.
- Claimed turning-point year: Not explicitly stated as a field-level turning-point year.
- Evidence quote (copy exact sentence + section):
  - Conclusions and Future Work: "Through experimental simulations of three real large-scale SDN topologies, the strategy proposed in this paper can obtain a multi-controller placement strategy ... with more negligible integrated latency, higher reliability and smaller overhead while maintaining load balancing."
  - Results comparison text: "Compared with the CPP scheme of the MOPSO algorithm ... reliability ... increases by about 10% ... overhead is reduced by 10%. Compared with ... NSGA-II ... reliability ... increases by about 7% ... overhead reduces by about 14%."

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
