#!/usr/bin/env python3
"""
Render the HTML poster to high-resolution print PDF and 300 DPI PNG using headless Google Chrome.
"""
import os
import subprocess
import time

POSTER_DIR = os.path.abspath(os.path.dirname(__file__))
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
    "file://" + HTML_PATH
]

print("Executing PDF generation...")
res_pdf = subprocess.run(cmd_pdf, capture_output=True, text=True, timeout=30)
if res_pdf.returncode == 0:
    print(f"✓ Successfully generated PDF: {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)")
else:
    print(f"PDF generation error: {res_pdf.stderr}")

# 2. Render high-res PNG (4K / 3370x2384 window size)
cmd_png = [
    "google-chrome",
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--window-size=3370,2384",
    "--screenshot=" + PNG_OUT,
    "--default-background-color=00000000",
    "--hide-scrollbars",
    "file://" + HTML_PATH
]

print("Executing PNG generation...")
res_png = subprocess.run(cmd_png, capture_output=True, text=True, timeout=30)
if res_png.returncode == 0:
    print(f"✓ Successfully generated PNG: {PNG_OUT} ({os.path.getsize(PNG_OUT)} bytes)")
else:
    print(f"PNG generation error: {res_png.stderr}")

print("Poster rendering complete!")

