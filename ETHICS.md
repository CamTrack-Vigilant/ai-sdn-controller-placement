# Research Ethics and Integrity Log

## Ethical Design Mandate

Principle: poor research design is unethical.

This project treats ethical practice as a design requirement, not a final checklist.
Every experiment should be reproducible, interpretable, and fairly reported.

## Scope of This Log

This log records how research quality, citation integrity, and data protection are maintained for:

- controller placement simulation experiments
- algorithm comparisons (baseline, heuristic, and AI methods)
- reporting and interpretation of findings

## Research Quality Controls

### Validity (Are we measuring what we claim?)

1. Construct validity
- Use explicit metrics tied to the research question: average latency, runtime cost, convergence behavior, and reliability metrics.
- Avoid claiming resilience improvements when only latency metrics were measured.

2. Internal validity
- Keep algorithm settings and scenario definitions consistent across comparisons.
- Use fixed seeds and repeated trials to limit random-noise bias.
- Record and disclose warm-up behavior to reduce startup timing distortion.

3. External validity
- Test across multiple topology families (Barabasi-Albert and Waxman) and node scales.
- Report where conclusions do and do not generalize.

### Reliability (Can the same process be repeated with similar outcomes?)

- Use version-controlled scripts and configuration defaults.
- Save raw, summary, and best-per-scenario outputs for each run.
- Capture seeds, trial counts, and algorithm budgets in output files.
- Run tests before major result collection.
- Document deviations from planned protocol in this log.

## Plagiarism Prevention and Attribution Protocol

I will not present borrowed ideas, formulations, or algorithm logic as original work.

### Mandatory attribution practices

- Cite primary algorithm sources in report chapters and README references.
- Add source comments when implementation logic follows specific papers/books.
- Distinguish between:
  - original project contributions (experiment design, integration, analysis)
  - established methods from prior literature

### Baseline citation register (to be used in report)

- Centralized reference register: references.md
- Use references.md as the single source for bibliography entries and attribution consistency checks.

### Pre-submission integrity check

Before sharing results with a supervisor or panel, verify:

- all borrowed equations and methods are cited
- all direct wording from sources is quoted or rewritten with citation
- algorithm novelty claims are accurate and not overstated

## Data Protection Plan (If Real Network Traffic Data Is Used)

Current state: the core experiments use synthetic topologies.

If real or semi-real traffic datasets are introduced, apply the following controls:

1. Data minimization
- Collect only features required for the research question.

2. De-identification
- Remove or hash direct identifiers (IP addresses, hostnames, user IDs, account IDs).
- Store key-mapping files separately and never commit them to source control.

3. Access control
- Keep sensitive raw data in protected storage with least-privilege access.
- Do not publish raw identifiable network traces in this repository.

4. Legal and institutional compliance
- Confirm permission to use the dataset.
- Obtain institutional ethics approval where required.
- Respect data-use agreements and retention policies.

5. Reporting protection
- Publish aggregated statistics and anonymized examples only.
- Avoid screenshots or logs that expose identifiable infrastructure details.

## Faculty Ethics Submission Controls (2026)

This project follows the two-stage ethics submission pathway.

| Ethics Gate | Deadline | Required Evidence | Status Rule |
| --- | --- | --- | --- |
| Interim protocol package to supervisors | 17 April 2026 | Ethics form, project summary, data protection plan, citation and integrity checklist | Must be submitted for review and revision feedback |
| Signed protocol to Faculty Research Ethics Committee | 27 April 2026 | Revised application, supervisor-approved corrections, required signatures | Final signed copy must be submitted by deadline |

## Submission Tracker (April 2026)

| Submission Item | Target Window | Required Artifacts | Owner | Status |
| --- | --- | --- | --- | --- |
| Supervisor Ethics Protocol Package | 14 to 17 April 2026 | Research Design; SDN controller scripts used as data collection tools (scripts/run_factorial_latency_cost_matrix.py and experiments/experiment_runner.py); docs/ethics/dataset_intake_form.md; docs/ethics/de_identification_checklist.md; docs/ethics/data_retention_schedule.md; docs/ethics/participant_consent_template.md | Candidate researcher | Pending |
| Signed Faculty Ethics Submission | By 27 April 2026 | Revised package with supervisor feedback and signatures | Candidate researcher and supervisors | Pending |

Hard boundary:

- No real or semi-real traffic data collection is permitted before formal ethics approval is in place.
- Until approval is confirmed, all experiments must remain on synthetic or fully public non-identifiable datasets.

## Presentation and Submission Compliance Checkpoints

| Programme Checkpoint | Date Window | Integrity Focus |
| --- | --- | --- |
| Draft proposal presentation | 13 or 20 April 2026 | Verify claims match available evidence and limitations are explicit |
| Proposal presentation | 18 or 25 May 2026 | Confirm methodology, citations, and ethics scope remain aligned |
| Progress presentation | 06 or 13 July 2026 | Report completed milestones and unresolved validity threats |
| 2nd progress or mock exam presentation | 28 September 2026 | Demonstrate methodological rigor and reproducibility readiness |
| Draft submission | 26 to 30 October 2026 | Complete integrity audit before pre-final submission |
| Final presentation or prototype demo | 04 to 06 November 2026 | Ensure demo and dissertation claims are fully traceable |
| Final corrected submission | 09 to 13 November 2026 | Include final paper output derived from research work |

## Weekly Integrity Checklist

Use this checklist at the end of each week:

- Research question and hypothesis for each run are explicit.
- Run parameters, seeds, and trial counts were logged.
- Results include both positive and negative findings.
- No unexplained exclusions of failed or weak runs.
- Citations for all non-original methods are present.
- Dataset handling complied with anonymization and access rules.
- Next week risks and mitigation steps are documented.

## Deviation and Incident Log

| Date | Planned Protocol | Deviation | Risk to Validity or Ethics | Corrective Action | Status |
| --- | --- | --- | --- | --- | --- |
| 2026-03-17 | Initial ethics framework setup | None | None | Baseline log established | Closed |
| 2026-04-17 | Interim ethics protocol to supervisors | Pending | Delayed supervisory review may affect faculty submission | Freeze package by 15 April and submit by 17 April | Open |
| 2026-04-27 | Signed protocol to Faculty Ethics Committee | Pending | Non-compliant data work if not approved on time | Submit revised signed protocol before deadline | Open |
