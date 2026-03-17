# Speaker Script: Draft Proposal Presentation (April 2026)

## Use Guide

- Intended duration: 10 to 12 minutes
- Read naturally, not word-for-word
- Keep one key message per slide

## Slide 1 Script: Title and Purpose

"Good day. My project is titled Multi-Objective Evaluation of AI-Driven Controller Placement in Multi-Site Software Defined Networks. The purpose is to determine when AI-based placement methods are truly better than classical methods, using reproducible and ethically grounded scientific comparison."

## Slide 2 Script: Problem and Motivation

"Controller placement is a core SDN decision because it affects how quickly the network responds, how robust it is during failures, and how much computational effort is needed to optimize it. In practice, decisions should not be made from only one metric. My work focuses on evaluating these trade-offs together."

## Slide 3 Script: Research Gap and Question

"The gap I identified is that many studies report improvements in one dimension, usually latency, without clearly disclosing computational cost or topology sensitivity. My primary question asks whether AI methods outperform baseline methods while remaining efficient and reliable across controlled multi-site scenarios."

## Slide 4 Script: Hypotheses and Contributions

"I test three hypotheses. First, AI can improve latency in selected scenarios. Second, those gains must be interpreted alongside runtime and convergence cost. Third, topology family and scale can change method ranking. My contribution is a reproducible benchmark and an efficiency frontier that supports practical decision-making instead of one-metric claims."

## Slide 5 Script: Methodology Design

"Methodologically, I use two synthetic topology families: Barabasi-Albert and Waxman. I compare five algorithms: random, greedy k-center, k-means, genetic, and bandit reinforcement learning. I run them in a factorial matrix over topology, node size, and controller budget, with fixed seeds and repeated trials for reproducibility."

## Slide 6 Script: Metrics and Decision Logic

"The key outputs are average latency, runtime in milliseconds, and convergence behavior for AI methods. For decision logic, I use Pareto-optimality and efficiency ranking. This ensures that a method is not called superior simply because it wins one metric while performing poorly on another."

## Slide 7 Script: Pilot Results Snapshot

"In the current pilot summary, genetic search achieved the best latency in both Barabasi-Albert and Waxman scenarios tested. However, greedy remained competitive in quality while being far cheaper in runtime in one scenario. Bandit RL was comparatively expensive in runtime in the pilot. So the early signal is not 'AI always wins', but rather 'AI gains are scenario-dependent and cost-sensitive'."

## Slide 8 Script: Ethics and Integrity Controls

"My ethical position is that poor design is unethical because it can lead to invalid claims. I therefore built controls for validity, reliability, attribution, and data protection. Two key gates are 17 April for supervisor ethics package submission and 27 April for signed faculty ethics submission. Until formal approval, experiments remain on synthetic or non-identifiable public data only."

## Slide 9 Script: Timeline and Delivery Plan

"The immediate timeline is draft proposal presentation in April, proposal presentation in May, progress checkpoint in July, and mock exam in September. Dissertation draft is targeted for late October, with final presentation and corrected submission in early to mid-November."

## Slide 10 Script: Closing and Feedback Request

"In closing, this project aims to produce decision-grade evidence on when AI controller placement is worth the computational overhead. I welcome feedback on whether my metrics, hypotheses, and evidence threshold are sufficient for proposal acceptance and ethics readiness. Thank you."

## Q&A Quick Responses

### Why not use only latency?

"Because real deployment decisions involve service continuity and operational cost. One metric alone can produce misleading recommendations."

### Why synthetic topologies first?

"Synthetic models allow controlled, reproducible baseline comparisons before extending to any sensitive or operational data."

### What if AI is slower but better in latency?

"That is exactly why we evaluate Pareto trade-offs. The recommendation depends on the acceptable cost-quality frontier for the target environment."

### What is your novelty?

"The novelty is not just algorithm use, but rigorous multi-objective evaluation with reproducibility, topology sensitivity, and ethics-governed reporting."
