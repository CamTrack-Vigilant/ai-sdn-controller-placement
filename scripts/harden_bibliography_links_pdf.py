#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import textwrap

import fitz


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INPUT_PDF = DOCS / "Research Proposal Template with Contant- PG Studies - Hons_linked.pdf"
OUTPUT_PDF = DOCS / "Research Proposal Template with Contant- PG Studies - Hons_linked_hardened.pdf"
REPORT_TXT = DOCS / "Research Proposal Template with Contant- PG Studies - Hons_bibliography_audit.txt"


@dataclass(frozen=True)
class RefEntry:
    anchor: str
    citation_token: str
    body: str
    primary_url: str
    oa_url: str | None = None


REF_ENTRIES = [
    RefEntry(
        anchor="ref-benoudifa",
        citation_token="Benoudifa et al., 2023",
        body=(
            "Benoudifa, M., Siad, L. and Belmokaddem, M. (2023) 'Autonomous solution for Controller "
            "Placement Problem of Software-Defined Networking using MuZero based intelligent agents', "
            "Journal of King Saud University - Computer and Information Sciences, 35(10), article 101842."
        ),
        primary_url="https://doi.org/10.1016/j.jksuci.2023.101842",
    ),
    RefEntry(
        anchor="ref-farahi",
        citation_token="Farahi et al., 2026",
        body=(
            "Farahi, I., et al. (2026) 'AP-DQN: A novel approach for controller placement in software-defined "
            "networks using deep reinforcement learning', Results in Engineering, 29, article 109631."
        ),
        primary_url="https://doi.org/10.1016/j.rineng.2026.109631",
    ),
    RefEntry(
        anchor="ref-heller",
        citation_token="Heller et al., 2012",
        body=(
            "Heller, B., Sherwood, R. and McKeown, N. (2012) 'The controller placement problem', Proceedings "
            "of the 1st Workshop on Hot Topics in Software Defined Networks (HotSDN), pp. 7-12."
        ),
        primary_url="https://doi.org/10.1145/2342441.2342444",
        oa_url="http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.297.6852",
    ),
    RefEntry(
        anchor="ref-radam",
        citation_token="Radam et al., 2022",
        body=(
            "Radam, N.S., Faraj Al-Janabi, S.T. and Jasim, K.Sh. (2022) 'Multi-Controllers Placement Optimization "
            "in SDN by the Hybrid HSA-PSO Algorithm', Computers, 11(7), p. 111."
        ),
        primary_url="https://doi.org/10.3390/computers11070111",
        oa_url="https://www.mdpi.com/2073-431X/11/7/111/pdf?version=1656931065",
    ),
    RefEntry(
        anchor="ref-lange",
        citation_token="Lange et al., 2015",
        body=(
            "Lange, S., Geissendorfer, S. and Suarez-Varela, S. (2015) 'POCO: A network placement controller "
            "using global optimization', Proc. ACM SIGCOMM, pp. 105-116."
        ),
        primary_url="https://doi.org/10.1145/2766498.2785234",
    ),
    RefEntry(
        anchor="ref-unizulu-ip",
        citation_token="University of Zululand, n.d.",
        body="University of Zululand (n.d.) 'Intellectual Property Policy'.",
        primary_url="https://www.unizulu.ac.za/policies/",
    ),
]

CITATION_MAP = {
    "Heller et al., 2012": "ref-heller",
    "Farahi et al., 2026": "ref-farahi",
    "Radam et al., 2022": "ref-radam",
    "Benoudifa et al., 2023": "ref-benoudifa",
    "Lange et al., 2015": "ref-lange",
}


def wrap_line(line: str, width: int) -> list[str]:
    return textwrap.wrap(line, width=width, break_long_words=False, break_on_hyphens=False)


def draw_reference_section(page: fitz.Page) -> list[str]:
    # Clear existing references body and draw clean section with hyperlinks.
    redact_rect = fitz.Rect(42, 58, 553, 820)
    page.add_redact_annot(redact_rect, fill=(1, 1, 1))
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    inserted_urls: list[str] = []

    y = 70.0
    page.insert_text((48, y), "15 REFERENCES (HARVARD STYLE)", fontname="helv", fontsize=11, color=(0, 0, 0))
    y += 18

    body_font = 8.3
    line_step = 10.2

    for entry in REF_ENTRIES:
        anchor_line = f'<a name="{entry.anchor}"></a>'
        page.insert_text((48, y), anchor_line, fontname="cour", fontsize=7.1, color=(0.35, 0.35, 0.35))
        y += 8.0

        for ln in wrap_line(entry.body, width=94):
            page.insert_text((48, y), ln, fontname="helv", fontsize=body_font, color=(0, 0, 0))
            y += line_step

        avail = f"Available at: {entry.primary_url}"
        page.insert_text((48, y), avail, fontname="helv", fontsize=body_font, color=(0.0, 0.2, 0.8))
        inserted_urls.append(entry.primary_url)
        y += line_step

        if entry.oa_url:
            oa = f"Open access: {entry.oa_url}"
            page.insert_text((48, y), oa, fontname="helv", fontsize=body_font, color=(0.0, 0.2, 0.8))
            inserted_urls.append(entry.oa_url)
            y += line_step

        y += 6.0

    return inserted_urls


def add_uri_links(page: fitz.Page, urls: list[str]) -> int:
    count = 0
    for url in urls:
        rects = page.search_for(url)
        for rect in rects:
            page.insert_link({"kind": fitz.LINK_URI, "from": rect, "uri": url})
            count += 1
    return count


def get_anchor_destinations(doc: fitz.Document) -> dict[str, tuple[int, fitz.Point]]:
    dests: dict[str, tuple[int, fitz.Point]] = {}
    for i, page in enumerate(doc):
        for entry in REF_ENTRIES:
            if entry.anchor in dests:
                continue
            probe = f'<a name="{entry.anchor}"></a>'
            rects = page.search_for(probe)
            if rects:
                r = rects[0]
                dests[entry.anchor] = (i, fitz.Point(r.x0, r.y0))
    return dests


def add_internal_citation_links(doc: fitz.Document, dests: dict[str, tuple[int, fitz.Point]]) -> int:
    total = 0
    for page in doc:
        for citation, anchor in CITATION_MAP.items():
            if anchor not in dests:
                continue
            probes = [f"[{citation}]", citation]
            seen: set[tuple[float, float, float, float]] = set()
            for probe in probes:
                for rect in page.search_for(probe):
                    key = (round(rect.x0, 1), round(rect.y0, 1), round(rect.x1, 1), round(rect.y1, 1))
                    if key in seen:
                        continue
                    seen.add(key)
                    page.insert_link(
                        {
                            "kind": fitz.LINK_GOTO,
                            "from": rect,
                            "page": dests[anchor][0],
                            "to": dests[anchor][1],
                        }
                    )
                    total += 1
    return total


def main() -> int:
    if not INPUT_PDF.exists():
        raise FileNotFoundError(f"Input PDF not found: {INPUT_PDF}")

    doc = fitz.open(INPUT_PDF)
    ref_page = doc[-1]

    urls = draw_reference_section(ref_page)
    uri_count = add_uri_links(ref_page, urls)

    dests = get_anchor_destinations(doc)
    goto_count = add_internal_citation_links(doc, dests)

    doc.save(OUTPUT_PDF, garbage=4, deflate=True)
    doc.close()

    lines = [
        f"Input: {INPUT_PDF}",
        f"Output: {OUTPUT_PDF}",
        "",
        "Anchor destinations:",
    ]
    for entry in REF_ENTRIES:
        if entry.anchor in dests:
            p, pt = dests[entry.anchor]
            lines.append(f"- {entry.anchor}: page {p + 1} @ ({pt.x:.1f}, {pt.y:.1f})")
        else:
            lines.append(f"- {entry.anchor}: NOT FOUND")
    lines += ["", f"URI links inserted: {uri_count}", f"Internal citation links inserted: {goto_count}"]

    REPORT_TXT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {OUTPUT_PDF}")
    print(f"Report: {REPORT_TXT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
