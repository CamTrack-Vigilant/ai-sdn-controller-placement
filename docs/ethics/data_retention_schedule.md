# Data Retention and Secure Disposal Schedule

This schedule operationalizes data lifecycle controls for the SDN controller placement project.

## Policy Basis

- Default retention period: 2 years from project closeout.
- If University of Zululand (UNIZULU) policy requires a longer period, follow the longer institutional requirement.
- The stricter rule always applies where policy and project practice differ.

## Data Classes and Retention Rules

| Data Class | Examples in This Project | Retention Period | Storage Requirement | Disposal Method |
| --- | --- | --- | --- | --- |
| Synthetic experiment data | Generated topology runs, benchmark CSV outputs | 2 years post-closeout | Version-controlled project storage | Cryptographic deletion of local copies where applicable; repository archival by policy |
| De-identified external data | Sanitized network traces approved for research use | 2 years post-closeout (or longer if UNIZULU requires) | Restricted encrypted storage with least privilege | Secure wipe and verified deletion certificate/log |
| Raw sensitive external data | Original identifiable traces and logs | Minimum feasible holding period during approved analysis only | Encrypted restricted storage, no public repo commits | Secure wipe using approved overwrite method; remove all backups |
| Ethics and approval records | Intake forms, approval letters, review checklists | 2 years post-closeout (or longer by institutional policy) | Controlled document storage | Secure document destruction after retention window |

## Operational Timeline

1. Intake stage
- Classify dataset with dataset_intake_form.md.
- Assign retention class before any analysis.

2. Active analysis stage
- Review access rights monthly.
- Maintain audit trail for sensitive data access.

3. Pre-submission stage
- Confirm only approved de-identified or synthetic data contributes to public outputs.

4. Closeout stage
- Start retention countdown from official project closeout date.
- Document disposal plan and responsible person.

5. Disposal stage
- Execute secure disposal actions.
- Record disposal evidence (date, method, reviewer).

## Secure Disposal Methods

- Secure digital overwrite for local files where technically applicable.
- Cryptographic key destruction for encrypted datasets.
- Verified deletion logs for restricted storage systems.
- Removal of residual copies in temporary folders and backups.

## Responsibilities

- Candidate researcher: maintain records, run scheduled reviews, execute disposal steps.
- Supervisor/co-supervisor: review compliance at milestone checkpoints.
- Ethics governance (if applicable): verify policy alignment for sensitive data classes.

## Retention Audit Log Template

- Dataset:
- Data class:
- Retention start date:
- Scheduled disposal date:
- Actual disposal date:
- Disposal method:
- Verified by:
- Notes:
