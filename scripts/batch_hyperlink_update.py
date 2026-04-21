#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import fitz


@dataclass(frozen=True)
class CitationTarget:
    citation: str
    reference_probe: str


ROOT = Path(__file__).resolve().parents[1]
TARGET_PDF = ROOT / "docs" / "submit" / "Research Proposal Template with Contant- PG Studies - Hons (1)_linked (6).pdf"
PDF_OUTPUT = ROOT / "docs" / "submit" / "Research Proposal Template with Contant- PG Studies - Hons (1)_linked (6)_hotlinks.pdf"
REPORT = ROOT / "docs" / "submit" / "hyperlink_batch_report.txt"

CITATION_TARGETS = [
    CitationTarget("Heller et al., 2012", "Heller, B."),
    CitationTarget("Farahi et al., 2026", "Farahi, I."),
    CitationTarget("Radam et al., 2022", "Radam, N.S."),
    CitationTarget("Benoudifa et al., 2023", "Benoudifa, M."),
    CitationTarget("Lange et al., 2015", "Lange, S."),
    CitationTarget("University of Zululand, n.d.", "University of Zululand"),
]

# Path-like code span: `foo/bar.py` or `foo\bar.py` or `folder/`
CODE_PATH_RE = re.compile(r"`([^`]*[\\/][^`]*)`")
# Standalone path-ish token in plain text (conservative)
PLAIN_PATH_RE = re.compile(r"(?<!\]\()(?<!`)(\.?\.?[\\/][\w .()\-\\/]+(?:\.[A-Za-z0-9]{1,6})?)(?!`)" )


def normalize_text_path(raw: str) -> str:
    s = raw.strip().strip("\"'")
    while s and s[-1] in ".,;:)]":
        s = s[:-1]
    return s.replace("\\", "/")


def resolve_workspace_target(path_text: str) -> Path | None:
    p = Path(path_text)
    candidates = []

    if p.is_absolute():
        candidates.append(p)
    else:
        candidates.append(ROOT / p)
        if str(path_text).startswith("./"):
            candidates.append(ROOT / path_text[2:])

    for c in candidates:
        if c.exists():
            return c.resolve()
    return None


def rel_link(from_doc: Path, to_target: Path) -> str:
    rel = to_target.relative_to(ROOT) if to_target.is_relative_to(ROOT) else to_target
    try:
        rel_from_doc = Path(".") / Path(Path(rel).as_posix())
        if from_doc.parent != ROOT:
            rel_from_doc = Path(".") / Path(Path(to_target.relative_to(from_doc.parent)).as_posix())
    except Exception:
        rel_from_doc = Path(".") / Path(Path(rel).as_posix())
    return rel_from_doc.as_posix()


def link_markdown_file(md_file: Path) -> tuple[int, int]:
    text = md_file.read_text(encoding="utf-8")
    original = text

    code_changes = 0
    plain_changes = 0

    def code_repl(match: re.Match[str]) -> str:
        nonlocal code_changes
        raw = match.group(1)
        norm = normalize_text_path(raw)
        target = resolve_workspace_target(norm)
        if target is None:
            return match.group(0)
        link = rel_link(md_file, target)
        label = raw.replace("\\", "/")
        code_changes += 1
        return f"[{label}]({link})"

    text = CODE_PATH_RE.sub(code_repl, text)

    # Avoid modifying existing markdown links and inline code by splitting around backticks.
    parts = text.split("`")
    for i in range(0, len(parts), 2):
        segment = parts[i]

        def plain_repl(match: re.Match[str]) -> str:
            nonlocal plain_changes
            raw = match.group(1)
            norm = normalize_text_path(raw)
            target = resolve_workspace_target(norm)
            if target is None:
                return raw
            link = rel_link(md_file, target)
            label = raw.replace("\\", "/")
            plain_changes += 1
            return f"[{label}]({link})"

        parts[i] = PLAIN_PATH_RE.sub(plain_repl, segment)

    text = "`".join(parts)

    if text != original:
        md_file.write_text(text, encoding="utf-8")

    return code_changes, plain_changes


def reference_destinations(doc: fitz.Document) -> dict[str, tuple[int, fitz.Point]]:
    dests: dict[str, tuple[int, fitz.Point]] = {}
    for ct in CITATION_TARGETS:
        for i, page in enumerate(doc):
            rects = page.search_for(ct.reference_probe)
            if rects:
                r = min(rects, key=lambda x: (x.y0, x.x0))
                dests[ct.citation] = (i, fitz.Point(r.x0, r.y0))
                break
    return dests


def add_pdf_links(input_pdf: Path, output_pdf: Path) -> dict[str, int]:
    doc = fitz.open(input_pdf)
    dests = reference_destinations(doc)
    counts = {ct.citation: 0 for ct in CITATION_TARGETS}

    for page in doc:
        for ct in CITATION_TARGETS:
            if ct.citation not in dests:
                continue
            probes = [f"[{ct.citation}]", ct.citation]
            seen: set[tuple[float, float, float, float]] = set()
            for probe in probes:
                for rect in page.search_for(probe):
                    key = (round(rect.x0, 1), round(rect.y0, 1), round(rect.x1, 1), round(rect.y1, 1))
                    if key in seen:
                        continue
                    seen.add(key)
                    doc_dest = dests[ct.citation]
                    page.insert_link(
                        {
                            "kind": fitz.LINK_GOTO,
                            "from": rect,
                            "page": doc_dest[0],
                            "to": doc_dest[1],
                        }
                    )
                    counts[ct.citation] += 1

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
    return counts


def verify_pdf_links(pdf_path: Path) -> tuple[int, int]:
    doc = fitz.open(pdf_path)
    total_links = 0
    good_links = 0
    for p in range(len(doc)):
        links = doc[p].get_links()
        total_links += len(links)
        for link in links:
            if link.get("kind") == fitz.LINK_GOTO and isinstance(link.get("page"), int):
                if 0 <= link["page"] < len(doc):
                    good_links += 1
            elif link.get("kind") == fitz.LINK_URI and link.get("uri"):
                good_links += 1
    doc.close()
    return total_links, good_links


def gather_docs() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "node_modules"} for part in p.parts):
            continue
        files.append(p)
    # Include text logs that are human-facing docs.
    for p in ROOT.rglob("*.txt"):
        if any(part in {".git", ".venv", "node_modules"} for part in p.parts):
            continue
        files.append(p)
    return sorted(set(files))


def main() -> int:
    if not TARGET_PDF.exists():
        raise FileNotFoundError(f"Missing target PDF: {TARGET_PDF}")

    pdf_counts = add_pdf_links(TARGET_PDF, PDF_OUTPUT)

    changed_files = 0
    code_link_total = 0
    plain_link_total = 0
    for doc in gather_docs():
        code_changes, plain_changes = link_markdown_file(doc)
        if code_changes or plain_changes:
            changed_files += 1
            code_link_total += code_changes
            plain_link_total += plain_changes

    total_links, good_links = verify_pdf_links(PDF_OUTPUT)

    lines = [
        f"Workspace: {ROOT}",
        f"Primary PDF input: {TARGET_PDF}",
        f"Primary PDF output: {PDF_OUTPUT}",
        "",
        "PDF citation links inserted:",
    ]
    for k, v in pdf_counts.items():
        lines.append(f"- {k}: {v}")

    lines += [
        "",
        f"Cross-document files updated: {changed_files}",
        f"Cross-document code-span links inserted: {code_link_total}",
        f"Cross-document plain-path links inserted: {plain_link_total}",
        "",
        f"PDF link verification: {good_links}/{total_links} links valid",
    ]

    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote PDF: {PDF_OUTPUT}")
    print(f"Wrote report: {REPORT}")
    print(f"Updated doc files: {changed_files}")
    print(f"PDF link verification: {good_links}/{total_links}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
