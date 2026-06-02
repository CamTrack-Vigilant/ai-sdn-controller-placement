# 🎨 How to Generate Flowchart Images
## Quick Start Guide

**Date:** April 28, 2026  
**Status:** All Mermaid diagram files created ✅

---

## 📁 Your Flowchart Files

```
docs/diagrams/
├── 01_complete_experimental_workflow.mmd        ← Diagram 1
├── 02_per_trial_measurement_protocol.mmd        ← Diagram 2
├── 03_phase4_analysis_pipeline.mmd             ← Diagram 3
├── 04_factorial_design_matrix.mmd              ← Diagram 4
└── README.md                                    (Full instructions)
```

All 4 diagrams are ready to convert to PNG/SVG/PDF images.

---

## 🚀 Fastest Way: Use Online Editor (No Installation)

### Step 1: Open Mermaid Live Editor
Visit: **https://mermaid.live**

### Step 2: Paste Diagram Content
1. Open any `.mmd` file from `docs/diagrams/`
2. Copy entire content
3. Paste into Mermaid Live Editor left panel
4. See diagram render on right panel instantly

### Step 3: Export to Image
Click menu (⋮) → **Download** → Choose:
- **PNG** (best for thesis)
- **SVG** (scalable, best for printing)
- **PDF** (for direct inclusion)

**Time required:** ~2 minutes per diagram

---

## 🖥️ Best Way for Batch Export: Use VS Code

### Step 1: Install Mermaid Extension
```
VS Code → Extensions → Search "Mermaid"
Install: "Mermaid" by jebbs
```

### Step 2: Open .mmd Files
```
File → Open Folder → Select docs/diagrams/
```

### Step 3: Preview & Export
For each file:
```
1. Right-click .mmd file
2. Select "Open Preview" or "Preview"
3. Right-click rendered diagram
4. Choose "Export as PNG" or "Export as SVG"
```

**Result:** 4 high-quality PNG files in `docs/diagrams/`

---

## 💻 For Developers: Command Line (If Installed)

### Install Mermaid CLI (Optional)
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Export All Diagrams at Once
```bash
cd /home/pro/Desktop/ai-sdn-controller-placement

# Convert all .mmd to PNG
for file in docs/diagrams/*.mmd; do
  mmdc -i "$file" -o "${file%.mmd}.png" -w 1600 -H 900
done

# Verify
ls -lh docs/diagrams/*.png
```

**Result:** 4 PNG files (1600×900 pixels)

---

## 📋 Summary: What Each Diagram Shows

### ✅ Diagram 1: Complete Experimental Workflow
- **Shows:** Full project from Phase 1 (Setup) → Phase 4 (Analysis)
- **Contains:** 30 seeds loop, 3 topologies, 3 budgets, 4 algorithms
- **Colors:** Green (start), Blue (phases), Gold (DQN), Orange (Greedy), Pink (cooldown)
- **Best for:** Defense presentation, thesis intro

### ✅ Diagram 2: Per-Trial Measurement Protocol  
- **Shows:** Step-by-step execution for each single trial
- **Contains:** Algorithm execution → L(P), R_avg(P), ω measurements → CSV recording
- **Colors:** Light blue (measurements), Gold (algorithm), Green (start/end)
- **Best for:** Implementation details, thesis methodology

### ✅ Diagram 3: Phase 4 Analysis Pipeline
- **Shows:** Post-experiment statistical analysis workflow
- **Contains:** Data aggregation → Descriptive stats → ANOVA → Pareto → Synthesis
- **Colors:** Light blue (main steps), Orange (ANOVA), Gold (Pareto), Green (synthesis)
- **Best for:** Thesis analysis chapter, defending analysis methodology

### ✅ Diagram 4: Factorial Design Matrix
- **Shows:** Experimental design structure with all 5 factors
- **Contains:** 4 Algorithms × 3 Topologies × 3 Budgets × 2 Scales × 30 Seeds
- **Colors:** Gold (title), Light blue (factors), Various (subcategories)
- **Best for:** Thesis methodology, explaining design rigor

---

## 🎯 Recommended Export Settings

**For Thesis (PDF/Print):**
```
Resolution: 1600×900 pixels
Format: PNG or SVG
DPI: 300 (if printable)
Background: White
```

**For Presentation (Slides):**
```
Resolution: 1600×900 pixels
Format: PNG
Aspect Ratio: 16:9
Background: Transparent or white
```

**For Web/GitHub:**
```
Resolution: 1200×800 pixels
Format: SVG (for scaling)
OR PNG (for compatibility)
```

---

## 📊 Expected Output

After exporting, you'll have:

```
docs/diagrams/
├── 01_complete_experimental_workflow.png      (~800 KB)
├── 02_per_trial_measurement_protocol.png      (~600 KB)
├── 03_phase4_analysis_pipeline.png            (~700 KB)
├── 04_factorial_design_matrix.png             (~650 KB)
└── [Or .svg versions if preferred]
```

---

## ✅ Next Steps

1. **Choose export method above** (Online editor = fastest)
2. **Export all 4 diagrams to PNG**
3. **Save to:** `docs/diagrams/`
4. **Embed in thesis** using:
   ```markdown
   ![Diagram Title](docs/diagrams/01_complete_experimental_workflow.png)
   ```

---

## 🔗 Useful Links

- **Mermaid Live Editor:** https://mermaid.live
- **Mermaid Documentation:** https://mermaid.js.org
- **VS Code Mermaid Extension:** https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml
- **Mermaid CLI Docs:** https://github.com/mermaid-js/mermaid-cli

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| Mermaid editor won't render | Try refreshing page or clear cache |
| PNG export is blurry | Use higher resolution (2000×1200) |
| Diagrams too large for slide | Resize: Use 1200×800 instead |
| Can't install mermaid-cli | Use online editor at mermaid.live (no install needed) |
| File not found error | Ensure you're in correct directory |

---

## 📞 Support

For detailed instructions, see:
- **docs/diagrams/README.md** - Full documentation
- **docs/VISUAL_FLOWCHART_REFERENCE.md** - How to use diagrams
- **docs/STUDY_DESIGN_METHODOLOGY.md** - Methodology section (Section 12)

---

**Version:** 1.0  
**Created:** April 28, 2026  
**Time to Export:** ~5-10 minutes (all 4 diagrams)  
**Ready for Thesis:** ✅ Yes

