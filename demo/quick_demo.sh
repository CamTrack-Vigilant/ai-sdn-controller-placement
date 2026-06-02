#!/usr/bin/env bash
set -euo pipefail
echo "Quick demo: repository checks and pilot summary"
echo
echo "1) Run quick verify"
python3 scripts/quick_verify.py
echo
echo "2) Show pilot summary"
python3 scripts/pilot_summary.py
echo
echo "3) Show pilot metrics (top-level)"
python3 -c 'import json,sys; print(json.dumps(__import__("json").loads(open("results/pilot_metrics.json").read())["metadata"], indent=2))'
