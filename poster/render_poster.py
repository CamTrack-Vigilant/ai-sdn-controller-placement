#!/usr/bin/env python3
"""
Render the HTML poster to high-resolution print PDF and 150 DPI PNG using headless Google Chrome and pdftoppm.
"""
import os
import shutil
import subprocess

WORKSPACE = "/home/pro/Desktop/ai-sdn-controller-placement"
POSTER_DIR = os.path.join(WORKSPACE, "poster")
DISS_DIR = os.path.join(WORKSPACE, "dissertation")
HTML_PATH = os.path.join(POSTER_DIR, "index.html")
PDF_OUT = os.path.join(POSTER_DIR, "POSTER_Thabang_Mhlokoma_UNIZULU_2026.pdf")
PNG_OUT = os.path.join(POSTER_DIR, "POSTER_Thabang_Mhlokoma_UNIZULU_2026.png")

print(f"Rendering poster from: {HTML_PATH}")

# 1. Render PDF (A0 Landscape: 1189mm x 841mm = 46.81in x 33.11in)
cmd_pdf = [
    "google-chrome",
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--print-to-pdf=" + PDF_OUT,
    "--print-to-pdf-no-header",
    "--paper-width=46.81",
    "--paper-height=33.11",
    "file://" + HTML_PATH,
]

print("Executing PDF generation...")
res_pdf = subprocess.run(cmd_pdf, capture_output=True, text=True, timeout=40)
if res_pdf.returncode == 0:
    print(f"✓ Successfully generated PDF: {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)")
else:
    print(f"PDF generation error: {res_pdf.stderr}")

# 2. Render PNG via pdftoppm
print("Rendering PNG via pdftoppm...")
tmp_page = os.path.join(POSTER_DIR, "poster_page")
cmd_png = ["pdftoppm", "-png", "-r", "150", PDF_OUT, tmp_page]
subprocess.run(cmd_png, capture_output=True, text=True, timeout=40)

gen_png = tmp_page + "-1.png"
if os.path.exists(gen_png):
    os.rename(gen_png, PNG_OUT)
    print(f"✓ Successfully generated PNG: {PNG_OUT} ({os.path.getsize(PNG_OUT)} bytes)")

for extra_pdf in [
    os.path.join(POSTER_DIR, "POSTER_Thabang_Buthelezi_UNIZULU_2026.pdf"),
    os.path.join(DISS_DIR, "Honours_Research_Poster_Thabang_Buthelezi.pdf"),
]:
    if os.path.exists(PDF_OUT):
        shutil.copy2(PDF_OUT, extra_pdf)
        print(f"✓ Synced PDF copy: {extra_pdf}")

for extra_png in [
    os.path.join(POSTER_DIR, "POSTER_Thabang_Buthelezi_UNIZULU_2026.png"),
    os.path.join(DISS_DIR, "Honours_Research_Poster_Thabang_Buthelezi.png"),
]:
    if os.path.exists(PNG_OUT):
        shutil.copy2(PNG_OUT, extra_png)
        print(f"✓ Synced PNG copy: {extra_png}")

print("Poster rendering complete!")
