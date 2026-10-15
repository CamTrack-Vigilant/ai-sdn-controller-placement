# Request for Paper Review: SATNAC 2026 Conference Submission

**Date:** 10 August 2026  
**To:** [Supervisor 1's Name / Title] & [Supervisor 2's Name / Title]  
**From:** [Your Name / Student ID]  
**Department:** Department of Computer Science & Telecommunications, University of Zululand  
**Subject:** Request for Review: SATNAC 2026 Research Paper Submission  

---

### Draft Email / Formal Letter Template

**Dear Prof./Dr. [Supervisor 1 Last Name] and Prof./Dr. [Supervisor 2 Last Name],**

I hope this email finds you well.

I am writing to formally request your guidance and expert review on my research paper manuscript prepared for submission to the **Southern African Telecommunication Networks and Applications Conference (SATNAC 2026)**.

The conference is being held under the official theme:  
> **"AI as the Last Mile: Building the Sustainable Digital Enterprise"**

Our paper targets the **Computer Science Technical Track** (*Programmable Infrastructure & AI for Network Optimization*).

---

### Paper Overview & Key Details

* **Paper Title:** *Decision-Grade Multi-Objective Benchmarking of DRL and Heuristic Controller Placement in Multi-Site Software Defined Networks*
* **Target Venue:** SATNAC 2026 (Full Research Paper, IEEE 2-Column Format)
* **Attached Documents:**
  1. **Camera-Ready Version:** [`SATNAC_RESEARCH_PAPER_CameraReady.docx`](file:///home/pro/Desktop/ai-sdn-controller-placement/docs/SATNAC_RESEARCH_PAPER_CameraReady.docx)
  2. **Anonymized Review Version:** [`SATNAC_RESEARCH_PAPER_Anonymized.docx`](file:///home/pro/Desktop/ai-sdn-controller-placement/docs/SATNAC_RESEARCH_PAPER_Anonymized.docx) (for EasyChair double-blind peer review)
  3. **Approved Research Proposal:** [`proposal.md`](file:///home/pro/Desktop/ai-sdn-controller-placement/docs/proposal.md) (for context and methodology mapping)

---

### What the Paper is About (Core Scientific Contributions)

This research addresses the **Controller Placement Problem (CPP)** in Software Defined WANs by providing a rigorous, empirical benchmark comparing Deep Reinforcement Learning (DRL) against classical heuristics.

While contemporary literature advocates DRL for network management, existing studies often ignore training overheads, energy consumption, or comparisons against static clustering algorithms. To solve this decision gap, our paper introduces:

1. **A 3-Axis Multi-Objective Optimization Framework:**
   * **Propagation Latency $L(P)$** in milliseconds ($\text{ms}$).
   * **Control-Plane Reliability $Reach_{avg}$**: Evaluated using an **$N-1$ single-link failure stress engine** (the mean fraction of switches remaining controller-reachable across all edge failures).
   * **Complexity Tax $\omega$**: Measured in seconds per episode ($\text{s/episode}$) to quantify computational energy overhead.

2. **Full Factorial & Canonical Topology Evaluation:**
   * Benchmarked across canonical reference backbones (**Internet2** with $N=20$, **ATT-MPLS** with $N=21$) and synthetic models (**Barabási-Albert**, **Waxman** up to $N=50$) under controller budgets $k \in \{3, 5\}$.
   * Evaluates 5 algorithm families: **Random Baseline, Greedy $K$-Center, $K$-Means Clustering, Genetic Algorithm (GA), and PyTorch Deep $Q$-Networks (DQN)**.

3. **Live Mininet OpenFlow Emulation:**
   * Validated on emulated Open vSwitch hardware with ICMP control probes to confirm real-world round-trip times (RTTs).

4. **Statistical Inferential Validation:**
   * Confirmed via 3-way factorial ANOVA ($F(4, 55) = 89.4, p < 0.001$), post-hoc Tukey HSD pairwise contrasts, and Cohen’s $d = 1.42$ effect sizes.

---

### Key Finding & Theme Alignment

The empirical results directly support the SATNAC 2026 theme by proving that **AI deployment must be computationally and economically justified**:
* For static WAN topologies ($N \le 50$), classical **$K$-Means clustering** and **Greedy $K$-Center** deliver optimal decision efficiency—achieving sub-3ms OpenFlow RTTs and $100\%$ $N-1$ failure reliability with $<5\text{ ms}$ compute runtime.
* PyTorch DQN policy convergence ($21.26\text{s}$, $\omega = 0.0213\text{ s/ep}$) yields negligible latency gain over $K$-Means on static graphs ($p = 0.68$). Therefore, DRL is strictly recommended when dynamic topology churn or multi-constraint failure recovery is present.

---

### Specific Review Feedback Requested

I would be extremely grateful if you could review the draft and provide feedback on:
1. **Methodological Framing & Rigor:** Whether the 3-axis formulation and statistical ANOVA presentation meet SATNAC standards.
2. **Clarity & Flow:** Suggestions on improving the abstract, discussion, and practical deployment guidelines.
3. **Submission Readiness:** Any adjustments needed before submitting to the EasyChair portal.

Thank you very much for your continuous guidance and support. I look forward to your feedback.

Warm regards,

**[Your Full Name]**  
BSc (Honours) Candidate  
Department of Computer Science & Telecommunications  
University of Zululand  
*Email:* [your.email@unizulu.ac.za]  
*Phone:* [Your Contact Number]  
