"""Diagnostics for BACI and component series."""

from __future__ import annotations

import pandas as pd
from scipy import stats


def event_frequency(series: pd.Series) -> dict[str, float | int]:
    """Count moderate and extreme months using one- and two-sigma thresholds."""
    clean = series.dropna()
    moderate = ((clean.abs() > 1.0) & (clean.abs() <= 2.0)).sum()
    extreme = (clean.abs() > 2.0).sum()
    total = len(clean)

    return {
        "total": int(total),
        "within_1sigma": int((clean.abs() <= 1.0).sum()),
        "moderate": int(moderate),
        "extreme": int(extreme),
        "moderate_pct": float(moderate / total * 100.0) if total else 0.0,
        "extreme_pct": float(extreme / total * 100.0) if total else 0.0,
    }


def linear_trend_per_decade(series: pd.Series) -> dict[str, float]:
    """Estimate an OLS trend in index units per decade."""
    clean = series.dropna()
    years = clean.index.year + (clean.index.month - 0.5) / 12.0
    result = stats.linregress(years, clean.to_numpy())
    return {
        "slope_per_year": float(result.slope),
        "slope_per_decade": float(result.slope * 10.0),
        "r_squared": float(result.rvalue**2),
        "p_value": float(result.pvalue),
    }
