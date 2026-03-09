from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def _pareto_mask_latency_reliability(latency: np.ndarray, reliability: np.ndarray) -> np.ndarray:
    """Return mask for non-dominated points (min latency, max reliability)."""
    keep = np.ones(len(latency), dtype=bool)

    for i in range(len(latency)):
        if not keep[i]:
            continue

        dominated_by_other = (
            (latency <= latency[i])
            & (reliability >= reliability[i])
            & ((latency < latency[i]) | (reliability > reliability[i]))
        )
        dominated_by_other[i] = False

        if dominated_by_other.any():
            keep[i] = False

    return keep


def mark_latency_reliability_pareto(
    df: pd.DataFrame,
    group_cols: Iterable[str] | None = None,
    latency_col: str = "average_distance",
    reliability_col: str = "control_plane_reliability",
    output_col: str = "is_pareto_optimal",
) -> pd.DataFrame:
    """
    Mark Pareto-optimal rows for latency/reliability trade-off.

    Optimization objective:
    - minimize latency_col
    - maximize reliability_col

    If group_cols is provided, Pareto front is computed independently per group.
    """
    if latency_col not in df.columns:
        raise ValueError(f"Missing latency column: {latency_col}")
    if reliability_col not in df.columns:
        raise ValueError(f"Missing reliability column: {reliability_col}")

    groups = list(group_cols or [])
    for col in groups:
        if col not in df.columns:
            raise ValueError(f"Missing group column: {col}")

    result = df.copy()
    result[output_col] = False

    if groups:
        grouped_iter = result.groupby(groups, sort=False, dropna=False)
    else:
        grouped_iter = [(None, result)]

    for _, group in grouped_iter:
        valid = group[[latency_col, reliability_col]].notna().all(axis=1)
        valid_group = group.loc[valid]
        if valid_group.empty:
            continue

        latency = valid_group[latency_col].to_numpy(dtype=float)
        reliability = valid_group[reliability_col].to_numpy(dtype=float)
        mask = _pareto_mask_latency_reliability(latency, reliability)

        result.loc[valid_group.index[mask], output_col] = True

    return result


def rank_latency_reliability_compromise(
    df: pd.DataFrame,
    group_cols: Iterable[str] | None = None,
    latency_col: str = "average_distance",
    reliability_col: str = "control_plane_reliability",
    distance_col: str = "ideal_point_distance",
    rank_col: str = "compromise_rank",
) -> pd.DataFrame:
    """
    Rank rows by normalized distance to the group ideal point.

    Ideal point per group:
    - latency at its minimum
    - reliability at its maximum

    Lower distance means a better compromise across both objectives.
    """
    if latency_col not in df.columns:
        raise ValueError(f"Missing latency column: {latency_col}")
    if reliability_col not in df.columns:
        raise ValueError(f"Missing reliability column: {reliability_col}")

    groups = list(group_cols or [])
    for col in groups:
        if col not in df.columns:
            raise ValueError(f"Missing group column: {col}")

    result = df.copy()
    result[distance_col] = np.nan
    result[rank_col] = np.nan

    if groups:
        grouped_iter = result.groupby(groups, sort=False, dropna=False)
    else:
        grouped_iter = [(None, result)]

    for _, group in grouped_iter:
        valid = group[[latency_col, reliability_col]].notna().all(axis=1)
        valid_group = group.loc[valid]
        if valid_group.empty:
            continue

        latency = valid_group[latency_col].to_numpy(dtype=float)
        reliability = valid_group[reliability_col].to_numpy(dtype=float)

        latency_min = float(latency.min())
        latency_max = float(latency.max())
        rel_min = float(reliability.min())
        rel_max = float(reliability.max())

        if latency_max > latency_min:
            latency_norm = (latency - latency_min) / (latency_max - latency_min)
        else:
            latency_norm = np.zeros_like(latency)

        if rel_max > rel_min:
            # Reliability is maximized, so distance is measured from group max.
            reliability_norm = (rel_max - reliability) / (rel_max - rel_min)
        else:
            reliability_norm = np.zeros_like(reliability)

        distances = np.sqrt(np.square(latency_norm) + np.square(reliability_norm))
        result.loc[valid_group.index, distance_col] = distances

        # Tie-break with latency (lower) then reliability (higher).
        sortable = valid_group.copy()
        sortable[distance_col] = distances
        sortable = sortable.sort_values(
            [distance_col, latency_col, reliability_col],
            ascending=[True, True, False],
        )
        ranks = pd.Series(np.arange(1, len(sortable) + 1), index=sortable.index)
        result.loc[sortable.index, rank_col] = ranks.astype(float)

    return result


def select_best_latency_reliability_compromise(
    df: pd.DataFrame,
    group_cols: Iterable[str] | None = None,
    latency_col: str = "average_distance",
    reliability_col: str = "control_plane_reliability",
    distance_col: str = "ideal_point_distance",
    rank_col: str = "compromise_rank",
) -> pd.DataFrame:
    """Return rank-1 compromise rows per group using ideal-point distance."""
    ranked = rank_latency_reliability_compromise(
        df,
        group_cols=group_cols,
        latency_col=latency_col,
        reliability_col=reliability_col,
        distance_col=distance_col,
        rank_col=rank_col,
    )

    best = ranked[ranked[rank_col] == 1].copy()
    groups = list(group_cols or [])
    sort_cols = groups + [latency_col, reliability_col]
    ascending = [True] * len(groups) + [True, False]
    if sort_cols:
        best = best.sort_values(sort_cols, ascending=ascending)
    return best
