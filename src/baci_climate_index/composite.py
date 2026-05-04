"""BACI composite construction and summary utilities."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

COMPONENT_ORDER = ("precipitation", "t90", "t10", "wind", "sealevel")


def build_baci(
    components: pd.DataFrame,
    *,
    sealevel_weight: float = 0.35,
) -> pd.Series:
    """Build the BACI composite from aligned component series."""
    missing_columns = sorted(set(COMPONENT_ORDER) - set(components.columns))
    if missing_columns:
        raise ValueError(f"Missing BACI component columns: {missing_columns}")

    baci = (
        components["t90"]
        - components["t10"]
        + components["precipitation"]
        + components["wind"]
        + sealevel_weight * components["sealevel"]
    ) / 5.0
    baci.name = "BACI"
    return baci


def require_complete_components(components: pd.DataFrame) -> None:
    """Raise if any component contains missing values."""
    nan_counts = components.isna().sum()
    if int(nan_counts.sum()) != 0:
        raise ValueError(f"Unexpected missing component values:\n{nan_counts}")


def reference_summary(
    components: pd.DataFrame,
    *,
    reference_start: str,
    reference_end: str,
) -> pd.DataFrame:
    """Return mean and standard deviation over the reference period."""
    ref_slice = components.loc[reference_start:reference_end, list(COMPONENT_ORDER)]
    return ref_slice.agg(["mean", "std"])


def summary_stats(series: pd.Series) -> dict[str, float | int]:
    """Return high-level descriptive statistics for a series."""
    clean = series.dropna()
    return {
        "count": int(clean.count()),
        "min": float(clean.min()),
        "max": float(clean.max()),
        "mean": float(clean.mean()),
        "std": float(clean.std()),
        "nan_count": int(series.isna().sum()),
    }


def decadal_means(series: pd.Series) -> pd.DataFrame:
    """Return mean BACI by decade."""
    return (
        series.to_frame("BACI")
        .assign(decade=series.index.year // 10 * 10)
        .groupby("decade")["BACI"]
        .mean()
        .to_frame("BACI_mean")
    )


def component_correlations(frame: pd.DataFrame) -> pd.DataFrame:
    """Return pairwise correlations for components and BACI."""
    return frame.dropna().corr()


def sealevel_weight_sensitivity(
    components: pd.DataFrame,
    *,
    weights: np.ndarray | None = None,
    base_weight: float = 0.35,
) -> pd.DataFrame:
    """Evaluate how BACI changes under alternative sea-level weights."""
    weights = weights if weights is not None else np.arange(0.0, 2.01, 0.25)
    base = build_baci(components, sealevel_weight=base_weight)

    rows = []
    for weight in weights:
        candidate = build_baci(components, sealevel_weight=float(weight))
        rows.append(
            {
                "sealevel_weight": float(weight),
                "mean": float(candidate.mean()),
                "std": float(candidate.std()),
                "corr_with_base": float(candidate.corr(base)),
            }
        )
    return pd.DataFrame(rows)


def fingerprint(series: pd.Series) -> dict[str, object]:
    """Return a compact reproducibility fingerprint."""
    return {
        "mean": float(series.mean()),
        "std": float(series.std()),
        "head": series.head(3).round(6).tolist(),
        "tail": series.tail(3).round(6).tolist(),
    }


def write_fingerprint(series: pd.Series, path: str | Path) -> dict[str, object]:
    """Write a BACI fingerprint JSON file and return the fingerprint."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    value = fingerprint(series)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
    return value
