#!/usr/bin/env python3
"""
Permanent Chat History Exporter
Extracts and converts the complete conversation transcript into a formatted
Markdown archive in docs/chat_history/ and archives raw JSONL transcripts.
"""

import os
import re
import json
import gzip
import shutil
from pathlib import Path
from datetime import datetime

CONVERSATION_ID = "e9e6736d-f7b8-426f-a005-6ac68c194a72"
APP_DATA_DIR = Path("/home/pro/.gemini/antigravity-ide")
LOG_DIR = APP_DATA_DIR / "brain" / CONVERSATION_ID / ".system_generated" / "logs"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "docs" / "chat_history"
RAW_LOG_DIR = OUTPUT_DIR / "raw_logs"

def export_chat():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_LOG_DIR.mkdir(parents=True, exist_ok=True)

    full_log_file = LOG_DIR / "transcript_full.jsonl"
    short_log_file = LOG_DIR / "transcript.jsonl"

    if not full_log_file.exists():
        print(f"Error: {full_log_file} does not exist.")
        return

    # 1. Archive raw logs with gzip compression
    print(f"[1/3] Archiving raw JSONL transcripts to {RAW_LOG_DIR}...")
    with open(full_log_file, "rb") as f_in, gzip.open(RAW_LOG_DIR / "transcript_full.jsonl.gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    if short_log_file.exists():
        with open(short_log_file, "rb") as f_in, gzip.open(RAW_LOG_DIR / "transcript.jsonl.gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print("  [OK] Compressed raw transcripts archived.")

    # 2. Parse turns from transcript_full.jsonl
    print("[2/3] Parsing conversation turns...")
    turns = []
    step_count = 0

    with open(full_log_file, "r", encoding="utf-8") as f:
        for line in f:
            step_count += 1
            entry = json.loads(line)
            t = entry.get("type")
            source = entry.get("source")

            if t == "USER_INPUT":
                content = entry.get("content", "")
                req_match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                req = req_match.group(1).strip() if req_match else content.strip()
                turns.append({
                    "role": "USER",
                    "step": entry.get("step_index", step_count),
                    "content": req
                })
            elif t == "PLANNER_RESPONSE":
                content = entry.get("content")
                if content and isinstance(content, str) and content.strip():
                    turns.append({
                        "role": "ASSISTANT",
                        "step": entry.get("step_index", step_count),
                        "content": content.strip()
                    })

    # 3. Generate Markdown document
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_slug = datetime.now().strftime("%Y-%m-%d")
    md_output_path = OUTPUT_DIR / f"{date_slug}_permanent_chat_history.md"

    print(f"[3/3] Generating permanent Markdown archive at {md_output_path}...")
    lines = [
        "# Permanent Session Transcript Archive: AI-SDN Controller Placement & Mini-Dissertation",
        "",
        f"- **Session ID:** `{CONVERSATION_ID}`",
        f"- **Archived On:** {timestamp_str}",
        f"- **Total Trajectory Steps:** {step_count}",
        f"- **Total Dialog Turns:** {len(turns)}",
        f"- **Raw Logs:** `docs/chat_history/raw_logs/transcript_full.jsonl.gz`",
        "",
        "---",
        "",
        "## Table of Contents",
        ""
    ]

    # Generate TOC
    user_turn_idx = 1
    for turn in turns:
        if turn["role"] == "USER":
            first_line = turn["content"].splitlines()[0][:80].strip()
            anchor = f"turn-{user_turn_idx}"
            lines.append(f"- [Turn {user_turn_idx}: {first_line}](#{anchor})")
            user_turn_idx += 1

    lines.append("")
    lines.append("---")
    lines.append("")

    # Generate Dialogue Body
    user_turn_idx = 1
    for turn in turns:
        if turn["role"] == "USER":
            lines.append(f"### <a id=\"turn-{user_turn_idx}\"></a>Turn {user_turn_idx} — User Prompt (Step {turn['step']})")
            lines.append("")
            lines.append("```text")
            lines.append(turn["content"])
            lines.append("```")
            lines.append("")
            user_turn_idx += 1
        elif turn["role"] == "ASSISTANT":
            lines.append(f"#### Antigravity Assistant Response (Step {turn['step']})")
            lines.append("")
            lines.append(turn["content"])
            lines.append("")
            lines.append("---")
            lines.append("")

    md_output_path.write_text("\n".join(lines), encoding="utf-8")
    md_size_kb = md_output_path.stat().st_size / 1024
    print(f"\n[SUCCESS] Permanent Chat History Saved!")
    print(f"  Markdown Archive: {md_output_path} ({md_size_kb:.1f} KB)")

if __name__ == "__main__":
    export_chat()
