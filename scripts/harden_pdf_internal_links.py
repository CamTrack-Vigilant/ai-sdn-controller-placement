#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INPUT_PDF = DOCS / "Research Proposal Template with Contant- PG Studies - Hons.pdf"
OUTPUT_PDF = DOCS / "Research Proposal Template with Contant- PG Studies - Hons_linked.pdf"
REPORT_TXT = DOCS / "Research Proposal Template with Contant- PG Studies - Hons_link_report.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add internal clickable links for in-text citations in a proposal PDF.")
    parser.add_argument("--input", type=Path, default=INPUT_PDF, help="Input PDF path")
    parser.add_argument("--output", type=Path, default=OUTPUT_PDF, help="Output PDF path")
    parser.add_argument("--report", type=Path, default=REPORT_TXT, help="Audit report text path")
    return parser.parse_args()


@dataclass(frozen=True)
class RefTarget:
    key: str
    entry_probe: str
    anchor_name: str


REF_TARGETS = {
    "heller": RefTarget("heller", "Heller, B.", "ref-heller"),
    "farahi": RefTarget("farahi", "Farahi, I.", "ref-farahi"),
    "radam": RefTarget("radam", "Radam, N.S.", "ref-radam"),
    "benoudifa": RefTarget("benoudifa", "Benoudifa, M.", "ref-benoudifa"),
    "lange": RefTarget("lange", "Lange, S.", "ref-lange"),
}

CITATION_MAP = {
    "Heller et al., 2012": "heller",
    "Farahi et al., 2026": "farahi",
    "Radam et al., 2022": "radam",
    "Benoudifa et al., 2023": "benoudifa",
    "Lange et al., 2015": "lange",
}

LANGE_ENTRY_LINE = (
    "Lange, S., Geissendorfer, S. and Suarez-Varela, S. (2015) "
    "'POCO: A network placement controller using global optimization', "
    "Proc. ACM SIGCOMM, pp. 105-116. doi: 10.1145/2766498.2785234."
)


def find_reference_page_range(doc: fitz.Document) -> tuple[int, int]:
    start = None
    end = len(doc) - 1
    for i, page in enumerate(doc):
        t = page.get_text("text")
        if "15 References" in t or "15 REFERENCES" in t:
            start = i
            break
    if start is None:
        start = max(0, len(doc) - 2)
    return start, end


def ensure_lange_entry(doc: fitz.Document, ref_start: int, ref_end: int) -> None:
    for i in range(ref_start, ref_end + 1):
        if doc[i].search_for("Lange, S."):
            return

    page = doc[ref_end]
    # Try a conservative insertion zone near bottom; reduce size until fit.
    rect = fitz.Rect(48, 700, 547, 818)
    for size in (9.0, 8.5, 8.0, 7.5):
        result = page.insert_textbox(rect, LANGE_ENTRY_LINE, fontname="helv", fontsize=size, color=(0, 0, 0))
        if result >= 0:
            return


def find_ref_destinations(doc: fitz.Document, ref_start: int, ref_end: int) -> dict[str, tuple[int, fitz.Point, fitz.Rect]]:
    dests: dict[str, tuple[int, fitz.Point, fitz.Rect]] = {}
    for key, ref in REF_TARGETS.items():
        for i in range(ref_start, ref_end + 1):
            rects = doc[i].search_for(ref.entry_probe)
            if rects:
                rect = min(rects, key=lambda r: (r.y0, r.x0))
                dests[key] = (i, fitz.Point(rect.x0, rect.y0), rect)
                break
    return dests


def add_internal_links(doc: fitz.Document, destinations: dict[str, tuple[int, fitz.Point, fitz.Rect]]) -> dict[str, int]:
    counts: dict[str, int] = {k: 0 for k in CITATION_MAP}

    for page_index, page in enumerate(doc):
        for citation, key in CITATION_MAP.items():
            if key not in destinations:
                continue

            # Match bracketed and non-bracketed forms to maximize coverage in PDF text extraction.
            probes = [f"[{citation}]", citation]
            seen_rects: set[tuple[float, float, float, float]] = set()
            for probe in probes:
                rects = page.search_for(probe)
                for rect in rects:
                    # Round geometry slightly to collapse probe-overlap duplicates.
                    rect_key = (round(rect.x0, 1), round(rect.y0, 1), round(rect.x1, 1), round(rect.y1, 1))
                    if rect_key in seen_rects:
                        continue
                    seen_rects.add(rect_key)
                    page.insert_link(
                        {
                            "kind": fitz.LINK_GOTO,
                            "from": rect,
                            "page": destinations[key][0],
                            "to": destinations[key][1],
                        }
                    )
                    counts[citation] += 1
    return counts


def write_report(
    destinations: dict[str, tuple[int, fitz.Point, fitz.Rect]],
    counts: dict[str, int],
    input_pdf: Path,
    output_pdf: Path,
    report_txt: Path,
) -> None:
    lines: list[str] = []
    lines.append(f"Input:  {input_pdf}")
    lines.append(f"Output: {output_pdf}")
    lines.append("")
    lines.append("Landing zones:")
    for key, ref in REF_TARGETS.items():
        if key in destinations:
            page, point, _ = destinations[key]
            lines.append(f"- {ref.anchor_name}: page {page + 1} @ ({point.x:.1f}, {point.y:.1f})")
        else:
            lines.append(f"- {ref.anchor_name}: NOT FOUND")
    lines.append("")
    lines.append("Injected links:")
    for citation, c in counts.items():
        lines.append(f"- {citation}: {c}")

    report_txt.parent.mkdir(parents=True, exist_ok=True)
    report_txt.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_pdf = args.input
    output_pdf = args.output
    report_txt = args.report

    if not input_pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_pdf}")

    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(input_pdf)
    ref_start, ref_end = find_reference_page_range(doc)

    ensure_lange_entry(doc, ref_start, ref_end)
    destinations = find_ref_destinations(doc, ref_start, ref_end)
    counts = add_internal_links(doc, destinations)

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()

    write_report(destinations, counts, input_pdf, output_pdf, report_txt)
    print(f"Wrote: {output_pdf}")
    print(f"Report: {report_txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
