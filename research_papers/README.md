# Research Papers Workspace

This folder is organized to help you extract and compare State of the Art (SotA) findings across SDN and related AI/networking papers.

## Folder Layout

- `research_papers/` - PDF papers and high-level workspace docs.
- `research_papers/sdn_textbooks/` - textbooks and long-form references.
- `research_papers/matrices/` - synthesis matrix CSV files.
- `research_papers/notes/` - paper-by-paper notes and extraction records.
- `research_papers/templates/` - reusable templates for consistent reviews.

## Workflow (Use This Every Time)

1. Read title, abstract, introduction, related work, and conclusion first.
2. Extract SotA indicators:
- Gold-standard models (examples: GPT-5, Llama-4, domain-specific model families).
- Best reported metric values (accuracy, F1, latency, efficiency gain).
- Turning-point year (when authors claim a paradigm shift).
3. Record findings into `matrices/sota_synthesis_matrix.csv`.
4. Classify each paper into:
- Technological SotA (best algorithms/models).
- Methodological SotA (how experiments are done).
- Functional SotA (what systems can do in real workflows).
5. Run the SotA vs Gap test:
- SotA statement: current ceiling in controlled settings.
- Gap statement: failure mode in real-world/noisy settings.

## Definition to Keep in Mind

- SotA = the current ceiling.
- Gap = where that ceiling cracks under realistic constraints.

## Immediate Next Step

1. Open `matrices/sota_synthesis_matrix.csv`.
2. Fill 3 papers completely first.
3. Compare recurring gaps and convert them into research questions.
