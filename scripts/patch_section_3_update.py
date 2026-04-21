"""
Patch Section 3.1 and 3.2 with hardened content.
Handles encryption by creating a new PDF output.
"""

import fitz
from pathlib import Path
import shutil

WORKSPACE = Path(r"c:\Users\fanele\AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks\ai-sdn-controller-placement")
DOCS = WORKSPACE / "docs"
PDF_IN = DOCS / "Research_Proposal_Hardened_Final.pdf"
PDF_OUT = DOCS / "Research_Proposal_Section3_Updated.pdf"
BACKUP = DOCS / "Research_Proposal_Before_Section3_Update.pdf"

HARDENED_3_1 = "SDN controller placement in multi-site environments is not primarily a problem of missing evidence; it is a quantifiable conflict between competing objectives. Lange et al. (2015) show that placement methods optimized around latency alone can fall short once reliability and operational cost are introduced, because the Pareto frontier reveals that no single configuration dominates across all criteria. This multi-objective conflict is not incidental; it is foundational to why method selection remains uncertain in practice. The unresolved problem is therefore not whether AI can outperform heuristics in isolated cases, but whether it can preserve its performance advantage while also remaining stable under link failures and across topology scales."

HARDENED_3_2 = "• Do AI-based controller placement methods preserve their latency advantage while improving reliability and computational cost along the Pareto frontier in multi-site SDN environments?\n• How do AI and heuristic methods compare in performance stability under link-failure dynamics across topology families and network scales?\n• For a given operational constraint set, which points on the latency-reliability-cost Pareto frontier are achievable by AI versus heuristics, and at what computational cost?"

def main():
    print("\n" + "="*70)
    print("  Section 3 Update: Problem Statement & Research Questions")
    print("="*70)
    
    # Backup
    shutil.copy(PDF_IN, BACKUP)
    print(f"\n✓ Backup: {BACKUP.name}")
    
    # Open and patch
    doc = fitz.open(PDF_IN)
    print(f"✓ Opened: {PDF_IN.name} ({len(doc)} pages)")
    
    # Page 4 (index 3) has both 3.1 and 3.2
    page = doc[3]
    
    try:
        # Patch 3.1: redact and insert
        print(f"\n📋 Patching 3.1 Problem Statement (Page 4)")
        rect_3_1 = fitz.Rect(68, 143, 550, 260)
        page.add_redact_annot(rect_3_1, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_textbox(rect_3_1, HARDENED_3_1, fontsize=11, fontname="helv", color=(0,0,0), align=fitz.TEXT_ALIGN_LEFT)
        print(f"  ✓ Inserted at 11pt")
        
        # Patch 3.2: redact and insert
        print(f"\n📋 Patching 3.2 Research Questions (Page 4)")
        rect_3_2 = fitz.Rect(68, 285, 550, 410)
        page.add_redact_annot(rect_3_2, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_textbox(rect_3_2, HARDENED_3_2, fontsize=10.5, fontname="helv", color=(0,0,0), align=fitz.TEXT_ALIGN_LEFT)
        print(f"  ✓ Inserted at 10.5pt")
        
        # Save (full PDF, not incremental)
        doc.save(str(PDF_OUT), garbage=4, deflate=True)
        doc.close()
        
        # Replace original
        shutil.move(PDF_OUT, PDF_IN)
        
        print(f"\n✓ Saved: {PDF_IN.name}")
        print("\n" + "="*70)
        print("Summary: 2/2 sections updated successfully")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        doc.close()

if __name__ == "__main__":
    main()
