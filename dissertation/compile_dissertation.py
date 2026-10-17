#!/usr/bin/env python3
"""
Compilation script for University of Zululand BSc Honours Mini-Dissertation.
Concatenates modular chapter markdown files into a master manuscript and compiles
to Microsoft Word (.docx) using Pandoc and the official department reference template.
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_DIR = PROJECT_ROOT / "dissertation"
DOCS_DIR = PROJECT_ROOT / "docs"
TEMPLATE_DOCX = DOCS_DIR / "Honours Mini-Dissertation Template (1).docx"

CHAPTERS = [
    "00_front_matter.md",
    "01_chapter_1_introduction.md",
    "02_chapter_2_literature_review.md",
    "03_chapter_3_methodology.md",
    "04_chapter_4_results_and_discussion.md",
    "05_chapter_5_conclusion.md",
    "06_references.md",
    "07_appendices.md",
]

MASTER_MD = DISSERTATION_DIR / "Honours_Mini_Dissertation_Thabang_Buthelezi.md"
OUTPUT_DOCX = DISSERTATION_DIR / "Honours_Mini_Dissertation_Thabang_Buthelezi.docx"

def compile_dissertation():
    print("=" * 80)
    print("COMPILING BSC HONOURS MINI-DISSERTATION: THABANG NHLOKOMA BUTHELEZI")
    print("=" * 80)

    # 1. Concatenate markdown files
    print(f"\n[1/3] Concatenating {len(CHAPTERS)} modular chapter files...")
    full_content = []
    total_words = 0
    total_lines = 0

    for ch_name in CHAPTERS:
        ch_path = DISSERTATION_DIR / ch_name
        if not ch_path.exists():
            print(f"  [ERROR] Missing chapter file: {ch_path}")
            sys.exit(1)
        
        content = ch_path.read_text(encoding="utf-8")
        lines = content.count("\n")
        words = len(content.split())
        total_lines += lines
        total_words += words
        print(f"  + Added {ch_name:<38} ({lines:>4} lines, {words:>5} words)")
        
        full_content.append(content)
        full_content.append("\n\n\\newpage\n\n")

    master_text = "".join(full_content)
    MASTER_MD.write_text(master_text, encoding="utf-8")
    print(f"\n[OK] Wrote Master Markdown: {MASTER_MD}")
    print(f"     Total Lines: {total_lines:,} | Total Words: {total_words:,}")

    # 2. Check pandoc availability
    print("\n[2/3] Checking Pandoc compilation environment...")
    try:
        pandoc_ver = subprocess.check_output(["pandoc", "--version"], text=True).splitlines()[0]
        print(f"  Pandoc detected: {pandoc_ver}")
    except Exception as e:
        print(f"  [ERROR] Pandoc not found or failed: {e}")
        sys.exit(1)

    # 3. Compile to DOCX using the official University of Zululand reference template
    print(f"\n[3/3] Compiling to Microsoft Word (.docx)...")
    print(f"  Reference Template: {TEMPLATE_DOCX}")
    print(f"  Target Document:    {OUTPUT_DOCX}")

    pandoc_cmd = [
        "pandoc",
        str(MASTER_MD),
        f"--reference-doc={TEMPLATE_DOCX}",
        "-o",
        str(OUTPUT_DOCX),
        "--toc",
        "--toc-depth=3",
    ]

    try:
        res = subprocess.run(pandoc_cmd, check=True, capture_output=True, text=True)
        if res.stdout:
            print("  Stdout:", res.stdout)
        if res.stderr:
            print("  Stderr:", res.stderr)
        
        docx_size_kb = OUTPUT_DOCX.stat().st_size / 1024
        print(f"\n[SUCCESS] Successfully compiled Mini-Dissertation!")
        print(f"  Output DOCX: {OUTPUT_DOCX} ({docx_size_kb:.1f} KB)")
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Pandoc compilation failed with code {e.returncode}:")
        print(e.stderr)
        sys.exit(1)

    print("\n" + "=" * 80)
    print("DISSERTATION COMPILATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    compile_dissertation()
