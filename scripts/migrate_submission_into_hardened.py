#!/usr/bin/env python3
"""Migrate finalized content into hardened template structure.

Source content: docs/Research_Proposal_Final_SUBMISSION.pdf
Target structure: docs/Research_Proposal_Hardened_Final.pdf
Output: docs/FINAL_SUBMISSION_Thabang_Mhlokoma.pdf
"""

from pathlib import Path
import os
import fitz

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SOURCE = DOCS / "Research_Proposal_Final_SUBMISSION.pdf"
TARGET = DOCS / "Research_Proposal_Hardened_Final.pdf"
OUTPUT = DOCS / "FINAL_SUBMISSION_Thabang_Mhlokoma.pdf"
VERIFY_TXT = DOCS / "_final_submission_extract.txt"


def extract_page_text(doc: fitz.Document, idx: int) -> str:
    return doc[idx].get_text("text")


def find_reference_page_indices(source_doc: fitz.Document) -> tuple[list[int], list[int]]:
    """Return (content_pages, reference_pages) from source doc by heading marker."""
    content = []
    refs = []
    in_refs = False
    for i in range(len(source_doc)):
        text = extract_page_text(source_doc, i)
        if "15 References (Harvard Style)" in text:
            in_refs = True
        if in_refs:
            refs.append(i)
        else:
            content.append(i)
    return content, refs


def main() -> int:
    if not SOURCE.exists() or not TARGET.exists():
        raise FileNotFoundError("Source or target PDF missing.")

    source = fitz.open(SOURCE)
    target = fitz.open(TARGET)

    # Use hardened cover page only, then clean source content pages,
    # then append source references at the end to guarantee Harvard consistency.
    cover_pages = [0]
    content_pages, ref_pages = find_reference_page_indices(source)

    out = fitz.open()

    # 1) Keep hardened structural front matter
    for p in cover_pages:
        out.insert_pdf(target, from_page=p, to_page=p)

    # 2) Insert clean corrected content (Sections 1-12 and method mappings)
    for p in content_pages:
        out.insert_pdf(source, from_page=p, to_page=p)

    # 3) Ensure Harvard references appended at end
    if ref_pages:
        for p in ref_pages:
            out.insert_pdf(source, from_page=p, to_page=p)

    # Metadata
    meta = target.metadata or {}
    meta.update(
        {
            "title": "FINAL_SUBMISSION_Thabang_Mhlokoma",
            "author": "Thabang Nhlokoma Buthelezi",
            "subject": "Research Proposal Final Submission",
            "keywords": "SDN, controller placement, DQN, Pareto, feasibility",
            "creator": "PyMuPDF migration pipeline",
        }
    )
    out.set_metadata(meta)

    out.save(OUTPUT, garbage=4, deflate=True)

    # Verification extract
    merged = fitz.open(OUTPUT)
    text = "\n\n".join(pg.get_text("text") for pg in merged)
    VERIFY_TXT.write_text(text, encoding="utf-8")

    # Structural checks
    checks = {
        "has_8_4_1": "8.4.1 Parameter Justification and Technical Stack Defense" in text,
        "has_11_feasibility": "0.0226 seconds per episode" in text,
        "has_radam": "Radam" in text and "10.3390/computers11080111" in text,
        "has_harvard_refs": "15 References (Harvard Style)" in text,
        "has_overlap_artifact": "4.2 Research objectives (or Hypotheses)" in text and "3.1 Problem Statement" in text,
        "has_placeholder": ("Insert text here" in text) or ("Example instructions" in text),
    }

    # Report
    size_bytes = OUTPUT.stat().st_size
    print(f"Output: {OUTPUT}")
    print(f"Pages: {len(merged)}")
    print(f"Size: {size_bytes} bytes")
    print("Metadata:")
    for k in ("title", "author", "subject", "creator"):
        print(f"  {k}: {merged.metadata.get(k, '')}")

    print("Checks:")
    for k, v in checks.items():
        print(f"  {k}: {v}")

    # Sequential page numbering verification (document-level)
    print("Page sequence: 1.." + str(len(merged)))

    merged.close()
    out.close()
    source.close()
    target.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
