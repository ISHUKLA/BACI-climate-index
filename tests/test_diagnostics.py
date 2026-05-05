from __future__ import annotations

import pandas as pd

from baci_climate_index.diagnostics import event_frequency


def test_event_frequency_uses_empirical_thresholds_by_default() -> None:
    series = pd.Series(range(100), index=pd.date_range("2000-01-01", periods=100, freq="MS"))

    result = event_frequency(series)

    assert result["method"] == "empirical Q80/Q95"
    assert result["total"] == 100
    assert result["moderate"] == 30
    assert result["extreme"] == 10
    assert result["moderate_pct"] == 30.0
    assert result["extreme_pct"] == 10.0


def test_event_frequency_can_use_gaussian_thresholds() -> None:
    series = pd.Series([-2.5, -1.5, -0.5, 0.0, 0.5, 1.5, 2.5])

    result = event_frequency(series, use_empirical=False)

    assert result["method"] == "gaussian 1sigma/2sigma"
    assert result["total"] == 7
    assert result["within_1sigma"] == 3
    assert result["moderate"] == 2
    assert result["extreme"] == 2
