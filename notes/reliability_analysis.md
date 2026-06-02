# Reliability Analysis Summary

Generated: results/rl_analysis/pareto/pareto_shortlist_reliability_sweep.json

Summary:

- Seeds checked: 42, 123, 456, 789, 999 (4-site × 12-node per site synthetic multi-site topology)
- For every shortlisted controller set the graph-only single-link-failure reliability was 1.0 across all seeds (no single-link failures caused controller disconnection in these synthetic topologies).
- Because the synthetic shortlist uses `s{site}-n{node}` labels, we additionally performed an Internet2 topology check using topology-native greedy k-center placements with the same controller budget.
- Internet2 check results: topology-native controllers `[0, 8, 6]` (node indices in the normalized Internet2 graph) produced reliability `1.0` for the same controller budget for the shortlist entries.

Notes / interpretation:

- A reliability value of `1.0` in the synthetic multi-site family indicates the controller sets are resilient to single-link failures in those generated graphs. This is plausible for multi-site topologies with redundant inter-site links.
- The Internet2 check used greedy k-center placements (topology-native) rather than reusing synthetic labels; it also returned `1.0` for the chosen k=3 placements. That means, for single-link failures measured by the current `control_plane_reliability_single_link_failure_cached` metric, the placement is robust for Internet2 too.
- Mininet Phase‑6 validation was executed in this environment but fell back to the synthetic RTT simulator because Mininet is not available here; the fallback produced reasonable RTT deltas (e.g., RTT minus graph distance ≈ 2.19 ms for the best candidate). A full Mininet emulation run will require system `mininet` and `sudo`.

Next recommended actions:

1) If you want a *real* packet-level validation, run the validator on a machine with system Mininet installed (see README notes). Example:

```bash
sudo apt-get update && sudo apt-get install -y mininet openvswitch-switch iperf3
source .venv/bin/activate
python scripts/validate_shortlist_mininet.py --benchmark-input results/experiment_data/benchmark_20260309_044937.csv --output results/rl_analysis/pareto/pareto_mininet_validation_mininet.json
```

2) To generate the presentation PDF locally (if not installed here), install `pandoc` or `wkhtmltopdf` and run one of:

```bash
# using pandoc
pandoc slides/presentation.md -o slides/presentation.pdf --resource-path=results/graphs

# or: convert markdown->html then html->pdf via wkhtmltopdf
python -m pip install markdown
python - <<'PY'
import markdown,sys
html = markdown.markdown(open('slides/presentation.md','r',encoding='utf-8').read())
open('slides/presentation.html','w',encoding='utf-8').write(html)
PY
wkhtmltopdf slides/presentation.html slides/presentation.pdf
```

3) If you want, I can attempt to run real Mininet here (will require `sudo`); confirm and I will try.
