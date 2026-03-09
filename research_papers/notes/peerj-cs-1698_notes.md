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
