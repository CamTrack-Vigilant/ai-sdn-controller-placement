# Reference Management Workflow & Citation Protocol

**Last Updated**: 23 March 2026  
**Project**: AI-Driven Controller Placement Optimization in Multi-Site SDN  
**Purpose**: Document the centralized reference management strategy and citation protocols for this research project

---

## Overview

This document describes how references and citations are managed throughout the ai-sdn-controller-placement project. It ensures academic integrity, prevents plagiarism, and maintains consistency across all research outputs.

**Key Principle**: Centralized Bibliography + Transparent Attribution = Defensible Research

---

## Central Repository: references.md

All bibliographic information for this project is consolidated in a single, authoritative file: **[references.md](../references.md)**

### Reference File Structure

The references.md file contains:

1. **Complete Citation List** (IEEE-formatted entries [1]-[8])
   - Fully vetted, published sources with complete metadata
   - Organized alphabetically by primary author surname
   - Each entry includes: authors, title, publication venue, volume/issue, pages, DOI

2. **Incomplete References** (Entries [A]-[D])
   - PDFs in research_papers/ folder that require full metadata extraction
   - Tracked for future completion before final submission
   - Status notes on metadata extraction progress

3. **Duplicate Source Mapping**
   - Identifies PDF files that refer to the same bibliographic source
   - Consolidates duplicates to single canonical entry
   - Example: Two downloaded copies of Heller et al. (2012) → tracked as one reference [1]

4. **Citation Pearl Growing Map**
   - Documents how seed papers (Heller et al., Gonzalez, Holland) were identified
   - Traces citation paths showing how child papers were discovered
   - Explains database selection and Boolean search strings used

5. **Search Strategy Documentation**
   - Lists all databases queried (IEEE Xplore, ACM Digital Library, Google Scholar, ResearchGate)
   - Documents Boolean search strings used for each research question
   - Records temporal scope (1985–2026), geographic scope (English-language), and exclusion criteria

### IEEE Reference Format (Mandatory)

All entries follow this format precisely:

```
[#] First Initial(s). Surname, et al., "Article title," Journal/Conference Title, vol. #, no. #, 
pp. page-range, Abbreviated Month Year, doi: DOI.
```

**Example**:
```
[1] B. Heller, R. Sherwood, and N. McKeown, "The controller placement problem," in Proceedings of 
the 1st Workshop on Hot Topics in Software Defined Networks (HotSDN). New York: ACM, Aug. 2012, 
pp. 7–12, doi: 10.1145/2342441.2342444.
```

**Why IEEE?** Consistency across computer science, networking, and engineering disciplines; required by many academic publishers and standards bodies.

---

## Citation Practices in Project Documents

### In-Text Citation Format

When referencing sources in proposal, README, or dissertation drafts, use **bracketed numerals** matching the reference number in references.md:

```
Several studies have proposed genetic algorithms for controller placement [6], [8], exploring populations 
of candidate placements and using recombination and mutation to navigate the search space [3].
```

**Guidelines**:
- Place citation bracket immediately after the claim it supports (before punctuation if standalone; after if integrated into text)
- Multiple citations can be combined: [6], [8] or [1]–[5] if citing a range
- If citing source for key methodological claim, cite at end of sentence or paragraph

### Claim-Citation Mapping (Anti-Plagiarism Check)

Every non-obvious factual claim must have a corresponding citation. Examples:

| Claim | Requires Citation? | Example Citation |
|-------|-------------------|------------------|
| "Greedy k-center algorithms deliver O(log n) approximation" | YES | [2] (Gonzalez 1985) |
| "SDN separates control and data planes" | NO (foundational knowledge) | Not required |
| "Heller et al. (2012) formalized controller placement as a facility location problem" | YES | [1] |
| "Genetic algorithms explore populations of candidate solutions" | YES (if explaining algorithm specifics) | [3] (Holland 1975) or [6] (Benoudifa application) |

**Orphan Statement Policy**: Any unsourced claim is flagged during review as requiring either: (a) citation to existing reference, (b) addition of new reference, or (c) removal if unsupported.

---

## Workflow: Adding a New Reference

When discovering a new source that merits inclusion:

1. **Extract Full Metadata**:
   - Authors (first initial + surname for all; et al. if >6 authors)
   - Title (exact capitalization)
   - Publication venue (journal title, conference name, publisher)
   - Volume, issue, page range, publication date
   - DOI (from journal website or doi.org lookup)

2. **Verify Source Quality**:
   - Is this peer-reviewed? (Prefer conference proceedings and journal articles)
   - Is it relevant to research questions? (Check abstract and introduction for SDN controller placement, optimization, or AI methods)
   - Does it add a new perspective or fill a gap identified in the Literature Review?

3. **Add to references.md**:
   - Assign next reference number [#] in sequence
   - Format using IEEE standard (see template above)
   - Add brief relevance note: "Addresses multi-objective evaluation in network optimization"
   - Place in alphabetical order by author surname
   - Update in-text citations in proposal if this source informs a claim

4. **Update Related Sections**:
   - If this reference introduces a new research area, consider adding a paragraph to the Literature Review explaining its contribution
   - If it supports a previously unsourced claim, add the citation [#] to that statement

5. **Audit Trail**:
   - Commit changes to references.md with clear message: "Add Ref [#] – LastName (Year) for [research topic]"
   - Update Literature Review section if new claim is introduced

---

## Reference Management Using Zotero (Recommended Tool)

**Zotero** (https://www.zotero.org/) is recommended for managing references, though not required for this project:

### Setting Up a Project Library

1. **Create a Zotero Collection**:
   - Create new Zotero group for "ai-sdn-controller-placement" project
   - Set collection to private or shared with supervisors
   - Enable full-text PDF indexing for searchability

2. **Import Existing References**:
   - Add all 8 complete references [1]-[8] from references.md
   - Attach PDF copies of papers to each entry (if available)
   - Tag by category: {baseline-heuristics}, {genetic-algorithms}, {reinforcement-learning}, {foundations}, {classical-theory}

3. **PDFs in research_papers/ Folder**:
   - Import incomplete PDFs [A]-[D] into Zotero
   - Use Zotero's metadata recognition to auto-extract bibliographic information
   - Manual corrections for author names, page numbers, etc.
   - Once complete, move to [#] numbered entry in references.md

4. **Export to IEEE Format**:
   - Use Zotero's "Export to Bibliography" function with IEEE CSL style
   - Paste exported entries into references.md
   - Verify formatting matches template exactly

### Ongoing Maintenance

- **Weekly**: Check Zotero library for new PDFs; extract metadata and add to references.md if relevant
- **Monthly**: Verify all in-text citations [#] are correctly numbered and correspond to actual entries in references.md
- **Before Submission**: Run final audit comparing Zotero library against references.md for consistency

---

## Citation Audit & Verification Checklist

Use this checklist before submitting any research output (proposal, dissertation, publication):

- [ ] All numbered references [#] cited in text match entries in references.md
- [ ] All entries in references.md follow IEEE format consistently
- [ ] No orphan claims exist (every substantive claim has a citation)
- [ ] All author names match exactly between text and references.md
- [ ] All page numbers, volumes, DOIs are included and correct
- [ ] No "ibid." or "op. cit." shortcuts; use [#] numbering exclusively
- [ ] URLs, if included, are permanent (use DOI when available; limit direct URLs)
- [ ] The "References Cited in [Section Name]" list at end of each section matches all [#] numbers in that section

---

## Examples: Common Citation Patterns in AI Research

### Pattern 1: Attributing Algorithm Invention
```
Greedy k-center algorithms for facility location problems were introduced by Gonzalez [2], 
who demonstrated an O(log n)-approximation ratio. This approach was later applied to SDN 
controller placement by Heller et al. [1].
```

### Pattern 2: Citing Methodological Foundation
```
This study employs a post-positivist quantitative paradigm [research methodology text], with 
deductive hypothesis testing through controlled experiments following established protocols in 
infrastructure optimization [1], [8].
```

### Pattern 3: Discussing Literature Gaps
```
While genetic algorithms [6] and reinforcement learning [7] have been proposed for controller 
placement, prior work lacks transparent multi-objective evaluation frameworks [1], [3], [4]. 
This study addresses that gap by...
```

### Pattern 4: Integrating Multiple Sources
```
The controller placement problem can be formalized as a facility location problem [1], [2], 
where optimizing latency [1] must be balanced against computational cost [6], [8] and reliability 
constraints [1]. However, most studies report latency in isolation [1], [3], creating a 
methodological gap [study claims].
```

---

## Tools and Software Notes

### Optional: Mendeley (Alternative to Zotero)

**Mendeley** (https://www.mendeley.com/) is an alternative reference manager:
- Web-based interface and desktop app
- Similar import/export capabilities to Zotero
- Integration with MS Word for in-text citations
- Ability to share libraries with collaborators

**Setup**: Same approach as Zotero; export to IEEE CSL format for consistency with references.md

### Plain Text / Git Approach (Minimal Setup)

If using Zotero/Mendeley is not feasible:
- Maintain references.md as the single source of truth (as is done in this project)
- Use plain-text editor to update entries
- Commit changes to Git repository with clear commit messages
- Cross-check in-text citations [#] manually before submission
- This project currently uses this approach ✓

---

## Troubleshooting & FAQs

**Q: I found a source that's not in references.md. How do I add it?**  
A: Follow the "Workflow: Adding a New Reference" section above. Extract metadata, verify quality, add to references.md with next [#] number, then add [#] citations to relevant claims in your text.

**Q: What if the PDF in research_papers/ doesn't have complete metadata?**  
A: Use Google Scholar to look up the paper by title or author. Paste the full citation into Google Scholar's "cite" function to get IEEE format. Add incomplete entries as [A]-[D] with a note that full metadata is pending.

**Q: Can I cite conference presentations or preprints?**  
A: Prefer peer-reviewed sources. If citing preprints, note the version and date clearly (e.g., "arXiv preprint, v2, March 2026"). Avoid citing unvetted blog posts or unaccredited web content.

**Q: What if two authors have the same surname?**  
A: Use first initial to disambiguate: "Smith, J." vs "Smith, M." in the reference list.

**Q: I want to quote a source directly. How do I cite that?**  
A: Use quotation marks around exact text, then cite the page number in square brackets: "This [claim]" [7, p. 42]. Add page number in references.md entries for sources with direct quotes.

---

## Integration with Dissertation Writing

When moving from proposal to dissertation:

1. **Copy references.md into dissertation folder** as the authoritative bibliography
2. **Maintain all [#] numbering** consistently across proposal and dissertation
3. **Before insertion into Word/LaTeX**: Verify all [#] numbers are sequential with no gaps
4. **Final bibliography generation**: Most word processors can auto-generate bibliography from numbered citations

---

## Academic Integrity Certification

This reference management workflow **supports compliance with**:
- University plagiarism prevention policy
- IEEE ethical standards for research integrity
- Open research transparency norms
- Reproducibility and verifiability principles

By maintaining a centralized, transparent, well-documented reference system, this project demonstrates **commitment to academic honesty** and **defensible, auditable research practices**.

---

**Next Steps for Project Maintainers**:
1. Verify that all [A]-[D] incomplete references are completed before final submission (target: post-29 March 2026)
2. Run final citation audit using checklist above
3. Confirm all claims in proposal, README, and RUNNING.md are properly sourced
4. Archive references.md and this protocol document with final submission

