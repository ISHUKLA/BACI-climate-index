"""Diagnostics for BACI and component series."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

try:
    from statsmodels.tsa.stattools import adfuller, kpss
except ModuleNotFoundError:  # pragma: no cover - exercised only without optional runtime deps
    adfuller = None
    kpss = None


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


def stationarity_tests(
    series: pd.Series,
    *,
    alpha: float = 0.05,
    kpss_regression: str = "c",
    min_observations: int = 12,
) -> dict[str, Any]:
    """
    Run ADF and KPSS stationarity tests on a BACI or component series.

    ADF H0: the series has a unit root, meaning it is non-stationary.
    KPSS H0: the series is stationary.

    Use kpss_regression="c" for level stationarity and "ct" for trend stationarity.
    """
    if kpss_regression not in {"c", "ct"}:
        raise ValueError('kpss_regression must be either "c" or "ct".')

    clean = (
        pd.to_numeric(series, errors="coerce")
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )
    n_observations = int(len(clean))

    result: dict[str, Any] = {
        "n_observations": n_observations,
        "alpha": float(alpha),
        "kpss_regression": kpss_regression,
    }

    if n_observations < min_observations:
        return {
            **result,
            "overall_conclusion": "insufficient data",
            "adf": _not_run("unit root / non-stationary", "insufficient data"),
            "kpss": _not_run("stationary", "insufficient data"),
        }

    values = clean.to_numpy(dtype=float)
    if np.allclose(values, values[0]):
        return {
            **result,
            "overall_conclusion": "constant series",
            "adf": _not_run("unit root / non-stationary", "constant series"),
            "kpss": _not_run("stationary", "constant series"),
        }

    adf_result = _run_adf(values, alpha)
    kpss_result = _run_kpss(values, alpha, kpss_regression)

    return {
        **result,
        "overall_conclusion": _combine_stationarity_conclusions(
            adf_result["conclusion"],
            kpss_result["conclusion"],
        ),
        "adf": adf_result,
        "kpss": kpss_result,
    }


def _run_adf(values: np.ndarray, alpha: float) -> dict[str, Any]:
    if adfuller is None:
        return _not_run("unit root / non-stationary", "statsmodels is not installed")

    try:
        statistic, p_value, _, _, critical_values, _ = adfuller(values, autolag="AIC")
    except Exception as exc:
        return _not_run("unit root / non-stationary", str(exc))

    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "critical_values": {key: float(value) for key, value in critical_values.items()},
        "conclusion": "stationary" if p_value <= alpha else "non-stationary",
        "null_hypothesis": "unit root / non-stationary",
    }


def _run_kpss(values: np.ndarray, alpha: float, regression: str) -> dict[str, Any]:
    if kpss is None:
        return _not_run("stationary", "statsmodels is not installed")

    try:
        statistic, p_value, _, critical_values = kpss(
            values,
            regression=regression,
            nlags="auto",
        )
    except Exception as exc:
        return _not_run("stationary", str(exc))

    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "critical_values": {key: float(value) for key, value in critical_values.items()},
        "conclusion": "non-stationary" if p_value < alpha else "stationary",
        "null_hypothesis": "stationary",
    }


def _not_run(null_hypothesis: str, error: str) -> dict[str, Any]:
    return {
        "statistic": None,
        "p_value": None,
        "critical_values": None,
        "conclusion": "not run",
        "null_hypothesis": null_hypothesis,
        "error": error,
    }


def _combine_stationarity_conclusions(adf_conclusion: str, kpss_conclusion: str) -> str:
    if adf_conclusion == "stationary" and kpss_conclusion == "stationary":
        return "likely stationary"
    if adf_conclusion == "non-stationary" and kpss_conclusion == "non-stationary":
        return "likely non-stationary"
    if "not run" in {adf_conclusion, kpss_conclusion}:
        return "inconclusive"
    return "mixed evidence"
