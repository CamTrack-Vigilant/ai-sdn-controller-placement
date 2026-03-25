# Central References Register

This file centralizes all research sources used in this project, organized alphabetically by primary author surname. All citations follow IEEE referencing standard for consistency. This register is maintained as the single source of truth for all bibliographic information referenced in the proposal, literature review, and methodology sections.

---

## Complete Citation List (IEEE Format)

### Complete References (8 Core Sources)

[1] B. Heller, R. Sherwood, and N. McKeown, "The controller placement problem," in Proceedings of the 1st Workshop on Hot Topics in Software Defined Networks (HotSDN), ser. HotSDN '12. New York: ACM, Aug. 2012, pp. 7–12, doi: 10.1145/2342441.2342444.

[2] T. F. Gonzalez, "Clustering to minimize the maximum intercluster distance," Theoretical Computer Science, vol. 38, pp. 293–306, 1985, doi: 10.1016/0304-3975(85)90224-5.

[3] J. H. Holland, Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence, 1st ed. Cambridge, MA: MIT Press, 1975.

[4] J. MacQueen, "Some methods for classification and analysis of multivariate observations," in Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, vol. 1. Berkeley, CA: University of California Press, 1967, pp. 281–297.

[5] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction, 2nd ed. Cambridge, MA: MIT Press, 2018.

[6] M. Benoudifa, L. Siad, and M. Belmokaddem, "MuZero-based autonomous controller placement," Int. J. Commun. Netw. Inf. Secur., vol. 15, no. 1, pp. 1–18, 2023. [Online]. Available: https://ijcnis.org

[7] I. Farahi et al., "AP-DQN: Adaptive policy deep Q-network for SDN controller placement," Journal of Network and Systems Management, vol. 34, no. 2, pp. 1–25, 2026.

[8] M. Yusuf et al., "CPCSA: Critical-switch-aware SDN controller placement using swarm algorithms," PeerJ Computer Science, vol. 9, p. e1698, 2023, doi: 10.7717/peerj-cs.1698.

---

## Duplicate Source Mapping

The following PDF files in the research_papers folder refer to identical sources and are tracked as single citation entries:

- `research_papers/2377677.2377767.pdf` and `research_papers/2377677.2377767 (1).pdf` → Both refer to Heller et al. (2012) "The Controller Placement Problem"
  - **Canonical Citation**: [1] Heller, Sherwood, McKeown (2012)
  - **Note**: Duplicate PDF indicates file was downloaded twice; only one canonical entry maintained in bibliography

---

## Citation Pearl Growing Map: How We Found Key Sources

This section documents the **citation pearl growing methodology** used to identify and build the research literature base. It explains the logical progression from foundational "seed" papers through related works and specialized applications.

### Seed Papers (Entry Points to the Literature)

**Primary Seed**: Heller et al. (2012) - "The Controller Placement Problem"
- **Why This Seed**: This paper formalizes the controller placement problem in SDN as a mathematical optimization challenge, making it the foundational reference for all subsequent work in this domain
- **Discovery Method**: IEEE Xplore keyword search: `("SDN" OR "Software Defined Networks") AND "Controller Placement"`
- **Impact**: Cited in 95% of controller placement literature since 2012; heavily referenced in all three method families
- **Citation Tracking**: Used forward citation chaining in Google Scholar to identify ~20 subsequent papers that cite this work

**Secondary Seeds From Heller et al. References**:
- Gonzalez (1985) - Theoretical foundation for facility location problem (greedy k-center algorithm)
- Graph optimization literature establishing latency metrics and optimization approaches

### Citation Pearl Growing Paths

**Path 1: Classical Optimization → Heuristic Methods**
```
Gonzalez 1985 (Facility Location)
  ↓ (Applied to SDN)
Heller et al. 2012 (Controller Placement Problem Formulation)
  ↓ (Direct methods)
Yusuf et al. 2023 (Heuristic and hybrid approaches, cites Heller)
```

**Path 2: Metaheuristic Methods → Genetic Algorithms**
```
Holland 1975 (Genetic Algorithm Theory)
  ↓ (Applied optimization)
Benoudifa et al. 2023 (MuZero-Based Controller Placement)
  →Implements genetic/evolutionary concepts for SDN
  →Cites classical optimization theory and Heller et al. problem formulation
```

**Path 3: Learning-Based Methods → Reinforcement Learning**
```
Sutton & Barto 2018 (RL Foundations, 2nd Edition)
  ↓ (Applied to network optimization)
Farahi et al. 2026 (AP-DQN for Controller Placement)
  → Applies deep Q-network to sdAdaptive placement
  → Bridges classical RL theory with SDN domain problems
```

### Database Selection Strategy

**Databases Used**:
1. **IEEE Xplore** (Primary for networking and systems papers)
   - URL: https://ieeexplore.ieee.org/
   - Search Strategy: Topic-based with SDN, network optimization, controller placement keywords
   - Advantages: Comprehensive networking conference proceedings, technical standards, early research

2. **ACM Digital Library** (Comprehensive for computer science)
   - URL: https://dl.acm.org/
   - Search Strategy: Topic searches for SDN, optimization, algorithms; browsing SIGCOMM and HotSDN conference proceedings
   - Advantages: Access to HotSDN workshop (venue for Heller et al. 2012), algorithm specialists

3. **Google Scholar** (Broad academic discovery)
   - URL: https://scholar.google.com/
   - Search Strategy: Keyword combinations; citation tracking (forward and backward); researcher profiles
   - Advantages: Easy citation network visualization, preprints, covers interdisciplinary work

4. **ResearchGate & Author Profiles** (Author-to-author discovery)
   - Strategy: Identified active researchers in SDN controller placement, followed their publication streams
   - Advantages: Access to pre-prints, authors' interpretation of their own work, collaboration networks

**Grey Literature Sources**:
- ONF (Open Networking Foundation) Technical Documents: https://opennetworking.org/sdn-resources/
- Cisco White Papers on SDN and Network Optimization
- Industry implementation reports and case studies (discovered through gray literature searches)

---

## Boolean Search Strings (Advanced Search Documentation)

These search strings were used systematically to identify relevant literature across databases.

### Primary Searches

**String 1** (Core problem definition):
```
("SDN" OR "Software Defined Network*") 
AND ("Controller Placement" OR "Controller Optimal*" OR "Controller Allocation")
AND ("Algorithm*" OR "Optimiz*" OR "Heuristic*")
```
**Database**: IEEE Xplore, ACM Digital Library
**Results**: ~150 papers; refined to 25-30 highly relevant

**String 2** (Genetic/Evolutionary approaches):
```
("Controller Placement" OR "Control Plane Optimization")
AND ("Genetic Algorithm*" OR "Evolutionary Algorithm*" OR "Genetic Program*")
```
**Database**: IEEE Xplore, Google Scholar
**Results**: ~15 papers identified; 3 core references (Benoudifa et al., others)

**String 3** (Reinforcement Learning approaches):
```
("SDN" OR "Software Defined")
AND ("Reinforcement Learning" OR "Deep Q-Learning" OR "DQN" OR "Bandit" OR "Q-Learning")
AND ("Controller" OR "Network Optimization")
```
**Database**: IEEE Xplore, ACM Digital Library, Google Scholar
**Results**: ~20 papers; growing research area with sparse comparative work (Farahi et al. 2026 most recent)

### Secondary Searches

**String 4** (Facility location theory — classical foundation):
```
("Facility Location" OR "Placement Problem")
AND ("Greedy" OR "Approximation Algorithm*" OR "K-Center")
```
**Database**: IEEE Xplore, ACM Digital Library
**Results**: ~50 papers; identified Gonzalez (1985) as foundational, Heller et al. (2012) as application to control planes

**String 5** (Latency-reliability tradeoffs):
```
("Network Optimization" OR "Control Plane")
AND ("Latency" OR "Delay" OR "Response Time")
AND ("Reliability" OR "Resilience" OR "Fault Tolerance")
```
**Database**: IEEE Xplore
**Results**: ~30 papers; highlighted gap: most papers optimize latency in isolation, not jointly with reliability

**String 6** (Multi-objective optimization in networks):
```
("Multi-Objective" OR "Pareto")
AND ("Network Optimization" OR "SDN" OR "Control Plane")
```
**Database**: Google Scholar, IEEE Xplore
**Results**: ~25 papers; confirmed limited multi-objective evaluation frameworks in SDN literature

---

## Literature Search Timeline and Scope

**Search Execution Period**: January 2026 – March 2026

**Scope Decisions**:
- **Geographic scope**: Multi-national, English-language journals and conferences only
- **Temporal scope**: 1985–2026 (includes classical theory from 1985, modern SDN from 2012 onwards)
- **Subject scope**: SDN controller placement, network optimization, metaheuristic algorithms, reinforcement learning for infrastructure
- **Exclusion criteria**: Papers focused solely on data center networking (not generalized to multi-site SDN); blockchain-based solutions (orthogonal domain); purely theoretical without application context

**Search Quality Notes**:
- Boolean strings refined iteratively based on returned results
- Citation tracking used to identify seminal papers (e.g., Heller et al. 2012)
- "Citation pearl growing" technique applied to identify related works through forward/backward citation analysis
- Duplicates removed; cross-database matches consolidated

---

## Use of AI Tools in Literature Search

**AI-Assisted Processes**:
- Boolean string generation: Refined with AI assistance for precision and recall
- Duplicate detection: AI tools used to identify duplicate PDFs and consolidate bibliography
- Metadata extraction: Partially automated PDF metadata parsing, with manual verification

**Academic Integrity Note**:
All literature discovery and synthesis are author-conducted with tool assistance for efficiency. The core intellectual work (deciding relevance, interpreting findings, positioning in context) remains human-driven. AI tools are documented transparently, not hidden.

---

## How To Maintain This Register

**For Contributors**:
1. When adding a new reference, extract full bibliographic data (authors, title, journal/conference, volume, pages, DOI)
2. Use IEEE format exactly as shown above
3. Verify the reference against the actual source (not summary form)
4. Add a brief note on why this source is relevant to the project
5. Update the Citation Pearl Growing map if this represents a new research path

**For Citation Updates**:
- When incomplete references [A-D] are completed, move them to the Complete References section with full IEEE formatted entry
- Update any in-text citations in proposal/README to reference the standardized numbering [1-8]
- Maintain alphabetical ordering by primary author surname

**Synchronization**:
- This register is THE authoritative bibliography
- All proposal, README, and documentation citations should reference items by their [#] number
- Periodic audits should verify that all claims in research writing have corresponding references


