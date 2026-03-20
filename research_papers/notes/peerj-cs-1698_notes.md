# Paper Extraction Template

## Basic Metadata

- Paper file: peerj-cs-1698.pdf
- Title: Controller placement with critical switch aware in software-defined network (CPCSA)
- Authors: Nura Muhammed Yusuf; Kamalrulnizam Abu Bakar; Babangida Isyaku; Abdelzahir Abdelmaboud; Wamda Nagmeldin
- Venue: PeerJ Computer Science
- Year: 2023
- Domain: SDN controller placement (SD-WAN / critical-switch aware)

## 1) SotA Indicators

- Gold-standard models mentioned: CPCSA (proposed) compared against SPDA, DBCP/DBCB, and gravCPA.
- Best metric reported: Aggregate reduction in controller overhead, packet loss, and latency, plus throughput improvement.
- Metric value: Aggregate improvements reported as 73% overhead reduction, 51% loss reduction, 16% latency reduction, and 16% throughput improvement; additional latency reductions include 27%/12%/3% against specific baselines in one scenario.
- Efficiency claim (if any): Critical-switch-aware partitioned placement reduces control overhead and improves latency-throughput tradeoff without changing network size.
- Claimed turning-point year: Not explicitly stated as a single field turning-point year.
- Evidence quote (copy exact sentence + section):
	- Abstract/conclusion claim: "The proposed solution has achieved an aggregate reduction in the controller's overhead by 73%, loss by 51%, and latency by 16% while improving throughput by 16% compared to the benchmark algorithms."
	- Results section snippet: "the proposed CPCSA reduces the average switch-to-controller latency by 27%, 12%, and 3%, respectively, compared to SPDA, DBCP, and gravCPA."

## 2) Synthesis Inputs

- Key capability demonstrated: Uses critical-switch awareness to reduce control overhead, packet loss, and latency while improving throughput.
- Main limitation acknowledged by authors: The authors note no support for heterogeneous controllers and no defense against vulnerabilities such as DDoS/common-mode faults.
- Data regime (size, quality, realism): Internet Topology Zoo topologies with simulation-based comparative measurements.
- Evaluation setting (controlled, synthetic, real-world): Controlled simulation with real topology inputs.

## 3) Categorized SotA

### Technological SotA
- Best algorithms/architectures: CPCSA partitioning and controller assignment guided by critical-switch role awareness.

### Methodological SotA
- Training/validation method: Comparative experimental evaluation on multiple metrics (overhead, loss, latency, throughput).
- Baselines compared against: SPDA, DBCP/DBCB, and gravCPA.

### Functional SotA
- What the system can do today: Improve placement quality where switch criticality strongly affects control-plane efficiency.
- What it still cannot do reliably: Address heterogeneous-controller settings and explicit adversarial fault/security scenarios.

## 4) SotA vs Gap Test

- SotA statement: Topology-role-aware placement can materially improve SDN control-plane efficiency in benchmark simulations.
- Gap statement: There is still limited evidence on reproducible compute-aware trade-offs and stability across broader scenario matrices.
- Why this gap matters for SDN controller placement research: Practical adoption requires methods that are not only better on quality metrics but also robust, efficient, and repeatable.

## 5) Your Notes

- Reusable ideas: Introduce node criticality features into baseline and AI placement policies.
- Risks/bias concerns: Criticality metrics may be topology-dependent and sensitive to modeling assumptions.
- Follow-up papers to read next: 2377677.2377767.pdf; 1-s2.0-S2590123026006717-main.pdf; symmetry-15-01520-v2.pdf.
