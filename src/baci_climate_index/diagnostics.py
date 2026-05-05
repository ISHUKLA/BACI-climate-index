"""Diagnostics for BACI and component series."""

from __future__ import annotations

import pandas as pd
from scipy import stats


def event_frequency(
    series: pd.Series,
    *,
    use_empirical: bool = True,
    q_moderate: float = 0.80,
    q_extreme: float = 0.95,
) -> dict[str, float | int | str]:
    """Count moderate and extreme months using empirical or Gaussian thresholds."""
    clean = series.dropna()

    if use_empirical:
        lo_mod = clean.quantile(1.0 - q_moderate)
        hi_mod = clean.quantile(q_moderate)
        lo_ext = clean.quantile(1.0 - q_extreme)
        hi_ext = clean.quantile(q_extreme)

        extreme_mask = (clean < lo_ext) | (clean > hi_ext)
        moderate_mask = ((clean < lo_mod) | (clean > hi_mod)) & ~extreme_mask
        method = f"empirical Q{int(q_moderate * 100)}/Q{int(q_extreme * 100)}"
    else:
        moderate_mask = (clean.abs() > 1.0) & (clean.abs() <= 2.0)
        extreme_mask = clean.abs() > 2.0
        method = "gaussian 1sigma/2sigma"

    moderate = moderate_mask.sum()
    extreme = extreme_mask.sum()
    total = len(clean)

    return {
        "method": method,
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
