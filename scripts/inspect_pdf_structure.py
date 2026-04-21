#!/usr/bin/env python3
import fitz

source = fitz.open("docs/Research_Proposal_Final_SUBMISSION.pdf")
hardened = fitz.open("docs/Research_Proposal_Hardened_Final.pdf")

print("SOURCE pages", len(source))
print("HARDENED pages", len(hardened))

for name, doc in (("SOURCE", source), ("HARDENED", hardened)):
    print("\n" + name + " page heads:")
    for i, page in enumerate(doc, start=1):
        lines = [x.strip() for x in page.get_text("text").splitlines() if x.strip()]
        head = " | ".join(lines[:6])[:180]
        print(f"{i:02d}: {head}")
