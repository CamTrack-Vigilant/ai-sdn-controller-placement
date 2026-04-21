#!/usr/bin/env python3
"""Render a clean final submission PDF from docs/proposal.md.

This avoids legacy patch overlays by rebuilding the document from audited source text.
"""

from pathlib import Path
import re
from xml.sax.saxutils import escape
import fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "docs" / "proposal.md"
OUT_PDF = ROOT / "docs" / "Research_Proposal_Final_SUBMISSION.pdf"

URL_PATTERN = re.compile(r'https?://[^\s<>"]+')
DOI_PATTERN = re.compile(r'\bdoi:\s*(10\.\d{4,9}/[^\s<>"]+)', re.IGNORECASE)
REFERENCE_LINKS = [
    (
        "https://doi.org/10.1016/j.jksuci.2023.101842",
        ["Benoudifa, M.", "MuZero-based autonomous controller placement"],
    ),
    (
        "https://doi.org/10.1016/j.rineng.2026.109631",
        ["Farahi, I.", "AP-DQN: Adaptive policy deep Q-network for SDN controller placement"],
    ),
    (
        "https://doi.org/10.1145/2342441.2342444",
        ["Heller, B.", "The controller placement problem"],
    ),
    (
        "https://doi.org/10.3390/computers11080111",
        ["Radam, N.S.", "Multi-Controllers Placement Optimization in SDN by the Hybrid HSA-PSO Algorithm"],
    ),
]


def make_clickable(text: str) -> str:
    escaped = escape(text)
    doi_placeholders = []

    def replace_doi(match: re.Match[str]) -> str:
        doi = match.group(1).rstrip(".,)")
        token = f"__DOI_LINK_{len(doi_placeholders)}__"
        doi_placeholders.append((token, f'doi: <a href="https://doi.org/{doi}"><u>{doi}</u></a>'))
        return token

    def replace_url(match: re.Match[str]) -> str:
        url = match.group(0).rstrip(".,)")
        return f'<a href="{url}"><u>{url}</u></a>'

    escaped = DOI_PATTERN.sub(replace_doi, escaped)
    escaped = URL_PATTERN.sub(replace_url, escaped)

    for token, doi_markup in doi_placeholders:
        escaped = escaped.replace(token, doi_markup)

    return escaped


def parse_markdown_lines(text: str):
    lines = text.splitlines()
    blocks = []
    para_buf = []
    list_buf = []

    def flush_para():
        nonlocal para_buf
        if para_buf:
            blocks.append(("p", " ".join(s.strip() for s in para_buf if s.strip())))
            para_buf = []

    def flush_list():
        nonlocal list_buf
        if list_buf:
            blocks.append(("ul", list_buf[:]))
            list_buf = []

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_para()
            flush_list()
            continue

        if line.startswith("#"):
            flush_para()
            flush_list()
            level = len(line) - len(line.lstrip("#"))
            blocks.append((f"h{level}", line[level:].strip()))
            continue

        if line.lstrip().startswith("- "):
            flush_para()
            list_buf.append(line.lstrip()[2:].strip())
            continue

        if line.strip().startswith("**") and line.strip().endswith("**"):
            flush_para()
            flush_list()
            blocks.append(("h5", line.strip().strip("*")))
            continue

        para_buf.append(line)

    flush_para()
    flush_list()
    return blocks


def build_pdf():
    text = SOURCE_MD.read_text(encoding="utf-8")

    # Purge known non-submission helper heading if present in source text.
    text = text.replace("## Reference Integrity Check (Technical Stack Defense)", "## 15 References (Harvard Style)")

    blocks = parse_markdown_lines(text)

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Times-Bold", fontSize=11.6, leading=13.4, spaceBefore=0, spaceAfter=0)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Times-Bold", fontSize=9.9, leading=11.5, spaceBefore=0, spaceAfter=0)
    h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Times-Bold", fontSize=9.0, leading=10.6, spaceBefore=0, spaceAfter=0)
    h4 = ParagraphStyle("H4", parent=styles["Heading4"], fontName="Times-Bold", fontSize=8.8, leading=10.2, spaceBefore=0, spaceAfter=0)
    h5 = ParagraphStyle("H5", parent=styles["Heading4"], fontName="Times-Bold", fontSize=8.8, leading=10.2, spaceBefore=0, spaceAfter=0)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Times-Roman", fontSize=8.5, leading=10.4, spaceAfter=0)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=8, firstLineIndent=0)

    story = []
    for kind, content in blocks:
        if kind == "h1":
            story.append(Paragraph(content, h1))
        elif kind == "h2":
            story.append(Paragraph(content, h2))
        elif kind == "h3":
            story.append(Paragraph(content, h3))
        elif kind == "h4":
            story.append(Paragraph(content, h4))
        elif kind == "h5":
            story.append(Paragraph(content, h5))
        elif kind == "p":
            # Lightweight cleanup of residual placeholders.
            if "insert text here" in content.lower() or "example instructions" in content.lower():
                continue
            story.append(Paragraph(make_clickable(content), body))
        elif kind == "ul":
            items = [ListItem(Paragraph(make_clickable(item), bullet), leftIndent=10) for item in content]
            story.append(ListFlowable(items, bulletType="bullet", start="-", leftIndent=8))
            story.append(Spacer(1, 0.1))

    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
        title="Research Proposal Final Submission",
        author="Thabang Nhlokoma Buthelezi",
    )
    doc.build(story)
    add_pdf_links()


def add_pdf_links():
    pdf = fitz.open(str(OUT_PDF))

    for ref_url, targets in REFERENCE_LINKS:
        targets = targets + [ref_url, ref_url.replace("https://doi.org/", "")]
        for page in pdf:
            for target in targets:
                for rect in page.search_for(target):
                    page.insert_link({"kind": fitz.LINK_URI, "from": rect, "uri": ref_url})

    temp_path = OUT_PDF.with_suffix(".tmp.pdf")
    pdf.save(str(temp_path), garbage=4, deflate=True)
    pdf.close()
    temp_path.replace(OUT_PDF)


if __name__ == "__main__":
    build_pdf()
    print(f"Rendered: {OUT_PDF}")
