#!/usr/bin/env python3
"""
Google AI Studio <-> Local Antigravity Agent Closed-Loop Bridge & Codebase Sync
===============================================================================
Synchronizes the local repository (`ai-sdn-controller-placement`) with the
Google AI Studio Cloud Agent and executes stateful multi-turn collaboration.

Features:
  - Generates `results/codebase_sync_manifest.json` and `docs/CODEBASE_CONTEXT_INDEX.md`
    containing exact Git branch, commit hash, file tree, SHA-256 checksums,
    experiment configurations, and core codebase summaries.
  - Verifies codebase parity between the Local Agent and Cloud Agent (`--sync`).
  - Supports attaching any set of repository files on demand (`--attach`).
  - Persists multi-turn state in `results/ai_studio_loop_state.json` and writes
    the latest Cloud Agent instructions to `docs/cloud_agent_inbox.md`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"
KEY_FILE = ROOT_DIR / "configs" / "ai_studio_key.txt"
SYSTEM_PROMPT_FILE = ROOT_DIR / "configs" / "ai_studio_system_prompt.md"
STATE_FILE = ROOT_DIR / "results" / "ai_studio_loop_state.json"
MANIFEST_FILE = ROOT_DIR / "results" / "codebase_sync_manifest.json"
INDEX_MD_FILE = ROOT_DIR / "docs" / "CODEBASE_CONTEXT_INDEX.md"
INBOX_FILE = ROOT_DIR / "docs" / "cloud_agent_inbox.md"
OUTBOX_FILE = ROOT_DIR / "docs" / "local_agent_outbox.md"

CORE_SYNC_FILES = [
    "configs/experiment_config.json",
    "algorithms/baseline/random_placement.py",
    "algorithms/baseline/greedy_placement.py",
    "algorithms/baseline/kmeans_placement.py",
    "algorithms/ai/genetic_algorithm.py",
    "algorithms/ai/reinforcement_learning.py",
    "evaluation/metrics.py",
    "evaluation/pareto.py",
    "simulation/mininet_simulation.py",
    "scripts/train_dqn_pilot.py",
    "scripts/run_stability_audit.py",
    "tests/test_rl_logging.py",
    "results/experiment_data/complete_proposal_aligned_benchmark.csv",
    "results/mininet_overhead_validation.json",
    "results/mininet_simulation_results.json",
]


def load_api_key() -> str:
    """Load GEMINI_API_KEY from environment, .env, or configs/ai_studio_key.txt."""
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key and env_key != "PASTE_YOUR_AI_STUDIO_API_KEY_HERE":
        return env_key

    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val and val != "PASTE_YOUR_AI_STUDIO_API_KEY_HERE":
                    return val

    if KEY_FILE.exists():
        for line in KEY_FILE.read_text(encoding="utf-8").splitlines():
            val = line.strip()
            if val and not val.startswith("#") and val != "PASTE_YOUR_API_KEY_ON_THIS_LINE":
                return val

    raise RuntimeError(
        "No valid GEMINI_API_KEY found in .env or configs/ai_studio_key.txt."
    )


def load_system_instruction() -> str:
    """Load system instructions for the Google AI Studio Cloud Agent."""
    if SYSTEM_PROMPT_FILE.exists():
        text = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()
        if text:
            return text
    return (
        "You are the Cloud Research & Architecture Agent on Google AI Studio, "
        "operating in a closed-loop partnership with the Local Antigravity Agent "
        "on the repository 'ai-sdn-controller-placement'."
    )


def build_codebase_manifest() -> Dict[str, Any]:
    """Build a deterministic SHA-256 manifest of all tracked repository files."""
    try:
        commit = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT_DIR)
            .decode("utf-8")
            .strip()
        )
        branch = (
            subprocess.check_output(
                ["git", "branch", "--show-current"], cwd=ROOT_DIR
            )
            .decode("utf-8")
            .strip()
        )
        remote = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], cwd=ROOT_DIR
            )
            .decode("utf-8")
            .strip()
        )
        tracked = (
            subprocess.check_output(["git", "ls-files"], cwd=ROOT_DIR)
            .decode("utf-8")
            .splitlines()
        )
    except Exception:
        commit, branch, remote, tracked = "unknown", "unknown", "unknown", []

    files_meta: List[Dict[str, Any]] = []
    for rel in sorted(tracked):
        fpath = ROOT_DIR / rel
        if not fpath.is_file():
            continue
        raw = fpath.read_bytes()
        sha256 = hashlib.sha256(raw).hexdigest()[:12]
        is_text = fpath.suffix.lower() in {
            ".py",
            ".md",
            ".json",
            ".csv",
            ".tex",
            ".txt",
            ".sh",
            ".yml",
            ".yaml",
            ".graphml",
            ".gml",
        }
        lines = raw.decode("utf-8", errors="ignore").count("\n") + 1 if is_text else None
        files_meta.append(
            {
                "path": rel,
                "size_bytes": len(raw),
                "lines": lines,
                "sha256_12": sha256,
            }
        )

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": remote,
        "branch": branch,
        "head_commit": commit,
        "total_tracked_files": len(files_meta),
        "files": files_meta,
    }
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Also generate human/LLM-readable CODEBASE_CONTEXT_INDEX.md
    md_lines = [
        "# Synchronized Codebase Context Index (`ai-sdn-controller-placement`)",
        "",
        f"- **Repository**: `{remote}`",
        f"- **Active Branch**: `{branch}`",
        f"- **HEAD Commit**: `{commit}`",
        f"- **Total Tracked Files**: `{len(files_meta)}`",
        f"- **Generated At**: `{manifest['generated_at']}`",
        "",
        "## 1. Tracked File Inventory (with SHA-256 Prefix & Line/Byte Counts)",
        "",
        "| Relative Path | Size (Bytes) | Lines | SHA-256 (12-char) |",
        "| :--- | :---: | :---: | :---: |",
    ]
    for item in files_meta:
        l_str = str(item["lines"]) if item["lines"] is not None else "binary"
        md_lines.append(
            f"| `{item['path']}` | {item['size_bytes']} | {l_str} | `{item['sha256_12']}` |"
        )

    md_lines.extend(
        [
            "",
            "## 2. Core Source & Benchmark Snapshots",
            "",
        ]
    )
    for rel in CORE_SYNC_FILES:
        fpath = ROOT_DIR / rel
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8", errors="replace")
            md_lines.append(f"### `{rel}`")
            md_lines.append("```")
            md_lines.append(text[:25000] + ("\n... [truncated]" if len(text) > 25000 else ""))
            md_lines.append("```")
            md_lines.append("")

    INDEX_MD_FILE.write_text("\n".join(md_lines), encoding="utf-8")
    return manifest


def load_loop_state() -> Dict[str, Any]:
    """Load stateful conversation history between Local Agent and Cloud Agent."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "turn_count": 0,
        "synced_commit": None,
        "previous_interaction_id": None,
        "history": [],
    }


def save_loop_state(state: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def call_ai_studio(
    api_key: str,
    prompt: str,
    system_instruction: str,
    state: Dict[str, Any],
    preferred_model: Optional[str] = None,
) -> Dict[str, Any]:
    """Send a turn to Google AI Studio with full conversation history."""
    env_model = None
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("AI_STUDIO_MODEL="):
                env_model = line.split("=", 1)[1].strip().strip('"').strip("'")

    candidate_models = (
        [preferred_model]
        if preferred_model
        else [
            m
            for m in [
                env_model,
                "gemini-4-argon",
                "gemini-3.8-flash",
                "gemini-3.5-flash",
                "gemini-2.5-flash",
            ]
            if m
        ]
    )

    contents: List[Dict[str, Any]] = []
    for item in state.get("history", [])[-6:]:
        user_txt = item.get("local_prompt", "")
        contents.append({"role": "user", "parts": [{"text": user_txt}]})
        contents.append({"role": "model", "parts": [{"text": item["cloud_response"]}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": contents,
    }
    data_bytes = json.dumps(payload).encode("utf-8")

    last_err = None
    for model in candidate_models:
        if not model:
            continue
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=240) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                candidates = body.get("candidates", [])
                parts = (
                    candidates[0].get("content", {}).get("parts", [])
                    if candidates
                    else []
                )
                text = "\n".join(p.get("text", "") for p in parts if "text" in p)
                return {
                    "model": model,
                    "interaction_id": body.get("responseId"),
                    "output_text": text.strip(),
                    "transport": "google-ai-studio-rest",
                }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code} on {model}: {e.read().decode('utf-8', errors='replace')}"
            continue
        except (TimeoutError, urllib.error.URLError) as e:
            last_err = f"Timeout/Network error on {model}: {e}"
            continue

    raise RuntimeError(f"Failed to reach Google AI Studio API: {last_err}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Google AI Studio <-> Local Antigravity Agent Loop Bridge & Codebase Sync"
    )
    parser.add_argument(
        "--ping",
        action="store_true",
        help="Send a handshake ping to verify the Google AI Studio connection.",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Build full codebase manifest and synchronize the Cloud Agent with the local repository state.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="",
        help="Message or instruction to send from Local Agent to Cloud Agent.",
    )
    parser.add_argument(
        "--attach",
        nargs="*",
        default=[],
        help="Optional workspace file paths to include in the payload.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override model name (optional).",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset multi-turn loop state.",
    )
    args = parser.parse_args()

    if args.reset:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("[OK] Reset Google AI Studio loop state.")
        return 0

    api_key = load_api_key()
    system_instruction = load_system_instruction()
    state = load_loop_state()
    manifest = build_codebase_manifest()

    attached_files = list(args.attach)
    if args.sync:
        if "docs/CODEBASE_CONTEXT_INDEX.md" not in attached_files:
            attached_files.insert(0, "docs/CODEBASE_CONTEXT_INDEX.md")
        if not args.prompt:
            user_prompt = (
                f"CODEBASE SYNCHRONIZATION CHECK (Commit `{manifest['head_commit']}` on branch `{manifest['branch']}`):\n"
                f"1. Before this sync, did you have direct access to our local filesystem, or are you receiving the codebase through this bridge?\n"
                f"2. Verify that you now have the full `{manifest['total_tracked_files']}`-file repository inventory, SHA-256 checksums, core algorithm implementations (`Random`, `Greedy K-Center`, `K-Means`, `GA`, `PyTorch DQN / Bandit RL`), `evaluation/metrics.py`, `simulation/mininet_simulation.py`, and benchmark datasets (`complete_proposal_aligned_benchmark.csv`, `mininet_overhead_validation.json`).\n"
                f"3. Confirm codebase parity using the structured sections (`[CODEBASE_SYNC_STATUS]`, `[CLOUD_AGENT_ANALYSIS]`, `[ACTION_ITEMS_FOR_LOCAL_AGENT]`) and identify any additional files from the inventory you want attached in the next turn."
            )
        else:
            user_prompt = args.prompt
    elif args.ping and not args.prompt:
        user_prompt = (
            "Handshake from Local Antigravity Agent in workspace "
            "'ai-sdn-controller-placement'. Confirm connection and state your "
            "readiness to collaborate in a closed loop."
        )
    elif args.prompt:
        user_prompt = args.prompt
    else:
        parser.print_help()
        return 1

    attached_blocks: List[str] = []
    for rel_path in attached_files:
        fpath = (
            (ROOT_DIR / rel_path).resolve()
            if not Path(rel_path).is_absolute()
            else Path(rel_path)
        )
        if fpath.exists():
            content = fpath.read_text(encoding="utf-8", errors="replace")
            attached_blocks.append(
                f"\n\n--- ATTACHED FILE: {fpath.relative_to(ROOT_DIR)} ---\n{content}\n--- END FILE ---"
            )

    full_payload = user_prompt + "".join(attached_blocks)

    OUTBOX_FILE.write_text(
        f"# Local Antigravity Agent Outbox\n\n"
        f"- **Timestamp**: `{datetime.now(timezone.utc).isoformat()}`\n"
        f"- **Commit**: `{manifest['head_commit']}` (`{manifest['branch']}`)\n"
        f"- **Attached Files**: `{attached_files}`\n\n"
        f"## Prompt Sent to Cloud Agent\n\n{user_prompt}\n",
        encoding="utf-8",
    )

    result = call_ai_studio(
        api_key=api_key,
        prompt=full_payload,
        system_instruction=system_instruction,
        state=state,
        preferred_model=args.model,
    )

    state["turn_count"] = int(state.get("turn_count", 0)) + 1
    state["synced_commit"] = manifest["head_commit"]
    if result.get("interaction_id"):
        state["previous_interaction_id"] = result["interaction_id"]
    state.setdefault("history", []).append(
        {
            "turn": state["turn_count"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": result["model"],
            "synced_commit": manifest["head_commit"],
            "local_prompt": user_prompt,
            "attached_files": attached_files,
            "cloud_response": result["output_text"],
        }
    )
    save_loop_state(state)

    inbox_md = (
        f"# Google AI Studio Cloud Agent Inbox (Turn {state['turn_count']})\n\n"
        f"- **Timestamp**: `{datetime.now(timezone.utc).isoformat()}`\n"
        f"- **Model**: `{result['model']}` (`{result['transport']}`)\n"
        f"- **Synchronized Commit**: `{manifest['head_commit']}` (`{manifest['branch']}`, `{manifest['total_tracked_files']}` tracked files)\n"
        f"- **Attached Files**: `{attached_files}`\n\n"
        f"## Local Agent Prompt\n\n{user_prompt}\n\n"
        f"## Cloud Agent Response\n\n"
        f"{result['output_text']}\n"
    )
    INBOX_FILE.write_text(inbox_md, encoding="utf-8")

    print(
        f"[OK] Synced & Connected to Google AI Studio ({result['model']}) — Turn {state['turn_count']} (Commit {manifest['head_commit'][:7]})"
    )
    print("-" * 72)
    print(result["output_text"])
    print("-" * 72)
    print(
        f"[OK] Updated {INBOX_FILE.relative_to(ROOT_DIR)}, {OUTBOX_FILE.relative_to(ROOT_DIR)}, and {MANIFEST_FILE.relative_to(ROOT_DIR)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
