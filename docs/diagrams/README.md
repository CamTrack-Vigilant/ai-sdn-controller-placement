# Visual Flowchart Diagrams
## AI-SDN Controller Placement Study

**Location:** `docs/diagrams/`  
**Format:** Mermaid markdown (.mmd)  
**Created:** April 28, 2026  

---

## 📊 Diagram Files

| File | Title | Purpose | Audience |
|------|-------|---------|----------|
| **01_complete_experimental_workflow.mmd** | Complete Experimental Workflow (Phase 1-4) | End-to-end project overview | All (supervisors, defense) |
| **02_per_trial_measurement_protocol.mmd** | Per-Trial Measurement Protocol | Step-by-step trial execution | Developers, readers |
| **03_phase4_analysis_pipeline.mmd** | Phase 4 Analysis Pipeline | Statistical analysis workflow | Analysts, thesis writers |
| **04_factorial_design_matrix.mmd** | Factorial Design Matrix Structure | Experimental design breakdown | All (methodology) |

| **Gemini_Generated_Image_offmw8offmw8offm (1).png** | Annotated Methodology Figure | Visual summary of heuristic vs DRL tracks, metric collection, and analysis pipeline | Proposal, thesis, defense slides |

---

## 🎨 How to View & Export Diagrams

### Annotated Methodology Figure

**File:** `Gemini_Generated_Image_offmw8offmw8offm (1).png`

**Use:** Insert this image into the methodology section of the proposal or thesis when you need the final annotated workflow visual.

**Suggested caption:**

> Figure 8.1. Annotated methodology diagram for the study. The figure shows the heuristic and DRL workflows, metric collection for ℓ, R, and ω, the aggregation bridge into Phase 3, the CPU thermal cooldown experimental condition, and the explicit no cross-seeding policy between heuristic solutions and DRL priors.

### Option 1: VS Code with Mermaid Extension (Recommended)
**Best for:** Quick viewing, editing, and live preview

```bash
# Install Mermaid extension in VS Code
# Extension ID: jebbs.plantuml
# Search: "Mermaid" in Extensions marketplace

# Then:
1. Open any .mmd file in VS Code
2. Right-click → "Open Preview"
3. Diagram renders in real-time
4. Export to PNG/SVG: Right-click preview → Export as PNG/SVG
```

### Option 2: Online Mermaid Editor
**Best for:** Quick viewing without installation

```
1. Visit: https://mermaid.live
2. Copy-paste content from any .mmd file into editor
3. See live diagram rendering
4. Click "Download" → Choose PNG, SVG, or PDF
```

### Option 3: Command-Line (mermaid-cli)
**Best for:** Batch conversion, CI/CD integration

```bash
# Install mermaid-cli globally
npm install -g @mermaid-js/mermaid-cli

# Convert single file to PNG
mmdc -i docs/diagrams/01_complete_experimental_workflow.mmd \
     -o docs/diagrams/01_complete_experimental_workflow.png

# Convert all files
for f in docs/diagrams/*.mmd; do
  mmdc -i "$f" -o "${f%.mmd}.png"
done
```

### Option 4: GitHub/GitLab Markdown Preview
**Best for:** Viewing in repositories

```
1. Push .mmd files to GitHub/GitLab
2. Mermaid automatically renders in markdown
3. No conversion needed
```

### Option 5: Jupyter Notebook Rendering
**Best for:** Integration with analysis notebooks

```python
# In Jupyter cell:
from mermaid import render_mmd
render_mmd(open('docs/diagrams/01_complete_experimental_workflow.mmd').read())
```

---

## 📥 Pre-Generated Export Instructions

### Batch Export to PNG (Recommended for Thesis)

```bash
#!/bin/bash
# Save as: export_diagrams.sh

cd /home/pro/Desktop/ai-sdn-controller-placement

# Create PNG versions (requires mermaid-cli installed)
for mmd_file in docs/diagrams/*.mmd; do
  png_file="${mmd_file%.mmd}.png"
  echo "Converting: $mmd_file → $png_file"
  mmdc -i "$mmd_file" -o "$png_file" -w 1600 -H 900
done

echo "✅ All diagrams exported to PNG (1600×900)"
ls -lh docs/diagrams/*.png
```

**Run it:**
```bash
chmod +x export_diagrams.sh
./export_diagrams.sh
```

---

## 🖼️ Embedding Diagrams in Thesis

### Markdown (Thesis Written in Markdown)
```markdown
# Methodology

## Study Design

![Complete Experimental Workflow](docs/diagrams/01_complete_experimental_workflow.mmd)

![Factorial Design Matrix](docs/diagrams/04_factorial_design_matrix.mmd)
```

### LaTeX (If thesis is in PDF/LaTeX)
```latex
\chapter{Methodology}

\section{Study Design}

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\textwidth]{docs/diagrams/01_complete_experimental_workflow.png}
  \caption{Complete Experimental Workflow (Phases 1-4)}
  \label{fig:workflow}
\end{figure}

\section{Factorial Design}

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\textwidth]{docs/diagrams/04_factorial_design_matrix.png}
  \caption{Factorial Design Matrix: 2,160 Experimental Cells}
  \label{fig:factorial}
\end{figure}
```

### PowerPoint/Slides (Defense Presentation)
```
1. Export all 4 diagrams to PNG (1600×900 resolution)
2. Insert PNGs into presentation slides
3. Use captions/notes to explain each diagram
4. Recommended slides:
   - Slide 3: Complete Workflow
   - Slide 4: Factorial Design
   - Slide 5: Measurement Protocol
   - Slide 6: Analysis Pipeline
```

### Google Docs/Word
```
1. Export to PNG: docs/diagrams/*.png
2. Insert → Image → Upload PNG files
3. Right-click → Wrap text
4. Add captions with numbering (Figure 1, Figure 2, etc.)
```

---

## 📋 Diagram Contents Summary

### Diagram 1: Complete Experimental Workflow
- **Sections:** 4 phases (Setup, Execution, Aggregation, Analysis)
- **Key Elements:** Nested loops, algorithm branching, thermal management
- **Total Nodes:** ~50+
- **Use In:** Defense intro, thesis Chapter 3, presentation opening

### Diagram 2: Per-Trial Measurement Protocol
- **Sections:** 4 measurement steps (L, R_avg, ω, secondary)
- **Key Elements:** Step-by-step execution, CSV recording
- **Total Nodes:** ~30+
- **Use In:** Thesis methodology detail, implementation guide

### Diagram 3: Phase 4 Analysis Pipeline
- **Sections:** 4 analysis steps (Aggregation, Descriptive, Inferential, Synthesis)
- **Key Elements:** ANOVA, Pareto, stability, cost-benefit
- **Total Nodes:** ~40+
- **Use In:** Thesis Chapter 4 (Analysis), presentation middle

### Diagram 4: Factorial Design Matrix
- **Sections:** 5 factors with levels, example cell, summary table
- **Key Elements:** Factor breakdown, experimental cell definition
- **Total Nodes:** ~25+
- **Use In:** Thesis methodology, presentation design section

---

## 🎯 Quick Reference: Which Diagram for What

| Use Case | Diagram(s) | Format |
|----------|-----------|--------|
| **Defense presentation (opening)** | 1, 4 | PNG 1600×900 |
| **Thesis methodology chapter** | 1, 2, 4 | PNG + inline text |
| **Thesis analysis chapter** | 3 | PNG + interpretation |
| **Implementation/coding** | 2 | MDD (raw) |
| **GitHub README** | 1, 4 | Auto-rendered MDD |
| **Conference paper** | 1, 3, 4 | High-res PNG (300 dpi) |
| **Internal documentation** | All 4 | MDD (editable) |

---

## 🔧 Customization & Editing

All diagrams are in human-readable Mermaid syntax. You can edit them directly:

```mermaid
# Example: Modify node color
style MYNODE fill:#FF6B6B  # Red
style MYNODE fill:#4ECDC4  # Teal
```

**Common edits:**
- Change colors (style definitions at bottom)
- Add/remove nodes (graph syntax at top)
- Update text/labels
- Modify flow logic

---

## 📦 File Manifest

```
docs/diagrams/
├── README.md  (this file)
├── 01_complete_experimental_workflow.mmd
├── 02_per_trial_measurement_protocol.mmd
├── 03_phase4_analysis_pipeline.mmd
├── 04_factorial_design_matrix.mmd
└── [PNG exports after running export script]
    ├── 01_complete_experimental_workflow.png
    ├── 02_per_trial_measurement_protocol.png
    ├── 03_phase4_analysis_pipeline.png
    └── 04_factorial_design_matrix.png
```

---

## 📖 Integration with Main Documentation

These diagrams are referenced in:
- **docs/STUDY_DESIGN_METHODOLOGY.md** (Section 12: Visual Flowcharts)
- **docs/VISUAL_FLOWCHART_REFERENCE.md** (Full reference guide)

---

## ✅ Export Checklist for Thesis Submission

- [ ] Diagram 1 exported as PNG (1600×900), file size < 2MB
- [ ] Diagram 4 exported as PNG (1600×900), file size < 2MB
- [ ] Diagrams embedded in thesis PDF with captions
- [ ] Figure references numbered (Figure 3.1, Figure 3.2, etc.)
- [ ] Captions include diagram title + brief description
- [ ] All diagrams render clearly in thesis (test PDF print)
- [ ] Backup: MDD source files stored in version control

---

**Version:** 1.0  
**Last Updated:** April 28, 2026  
**Status:** Ready for export and thesis integration

