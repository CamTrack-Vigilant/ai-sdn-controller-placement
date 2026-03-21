# De-Identification Checklist (SDN Data)

Use this checklist before storing, analyzing, or publishing any non-synthetic SDN dataset.

## Scope

- Dataset name:
- Dataset version/date:
- Reviewer:
- Review date:
- Linked intake form:

## A. Direct Identifier Controls

- IP addresses masked, tokenized, or irreversibly hashed.
- MAC addresses masked, tokenized, or irreversibly hashed.
- Device serial numbers removed or replaced with pseudonymous IDs.
- Hostnames sanitized to non-identifying aliases.
- User, account, tenant, or operator identifiers removed.
- API keys, tokens, certificates, and secrets removed.

## B. SDN Topology Re-Identification Risks

- Exact node labels replaced with abstract node IDs.
- Site names, building names, and rack identifiers removed.
- Controller endpoint addresses abstracted.
- Edge lists reviewed for critical infrastructure disclosure risk.
- Rare-path or unique-topology signatures generalized where necessary.
- Geo-coordinates reduced to coarse region (or removed).

## C. Temporal and Event Trace Risks

- High-resolution timestamps coarsened where possible.
- Event sequences reviewed for linkage attacks.
- Outlier events that uniquely identify infrastructure removed or generalized.
- Security incident references sanitized.

## D. Data Utility vs. Privacy Balance

- Metrics needed for controller placement analysis preserved.
- Latency, reliability, and load metrics still valid after de-identification.
- Data transformations documented for reproducibility.
- Risk of reverse engineering assessed as acceptable.

## E. Storage and Access Safeguards

- Raw pre-processed data kept in restricted storage only.
- De-identified working copy separated from raw source.
- Access control set to least privilege.
- Access log enabled for sensitive datasets.
- Backup copies inherit same protection controls.

## F. Publication and Sharing Controls

- No raw identifiable traces included in repository.
- Only aggregate outputs and anonymized examples prepared for publication.
- Figures/tables checked for leakage of identifiers.
- External sharing terms aligned with license and ethics approval.

## G. Final Decision

- De-identification complete: Yes / No
- Residual risk level: Low / Moderate / High
- Additional action required:
- Approved for analysis by:
- Approval date:
