# Research Notes

## Experiment Tracking

- Keep a log per run: topology parameters, algorithm settings, seed, timestamp.
- Store generated metrics and plot references with each run.

## Open Questions

- How many controllers are optimal per site count and density level?
- Does AI consistently outperform greedy placement under failures?
- Which algorithms are most stable across random seeds?

## Immediate To-Do

- Integrate Mininet for packet-level validation.
- Add confidence intervals for key metrics.
- Introduce dynamic traffic/load scenarios.

## Methodology Definitions

- Average latency distance:

```text
D_avg(C) = (1 / |V|) * sum_{v in V} min_{c in C} d(v, c)
```

- Control-plane reliability under single-link failure:

```text
R_link(C) = (1 / |E|) * sum_{e in E} ( |Reach(V, C, G - e)| / |V| )
```

- Composite bandit reward used for reward shaping:

```text
Reward(C) = -(w_lat * D_avg(C)) + (w_rel * R_link(C))
```

Where `C` is controller placement, `V` is node set, `E` is edge set, and
`Reach(V, C, G-e)` is the subset of nodes in `G-e` that can reach at least one controller.
