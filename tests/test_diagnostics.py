from __future__ import annotations

import numpy as np
import pandas as pd

import baci_climate_index.diagnostics as diagnostics


def test_stationarity_tests_combines_adf_and_kpss(monkeypatch) -> None:
    def fake_adfuller(values, autolag):
        assert autolag == "AIC"
        np.testing.assert_array_equal(values, np.arange(12.0))
        return -4.0, 0.01, 0, 12, {"1%": -3.5, "5%": -2.9, "10%": -2.6}, None

    def fake_kpss(values, regression, nlags):
        assert regression == "c"
        assert nlags == "auto"
        np.testing.assert_array_equal(values, np.arange(12.0))
        return 0.1, 0.1, 0, {"1%": 0.7, "5%": 0.46, "10%": 0.35}

    monkeypatch.setattr(diagnostics, "adfuller", fake_adfuller)
    monkeypatch.setattr(diagnostics, "kpss", fake_kpss)

    result = diagnostics.stationarity_tests(pd.Series(np.arange(12.0)))

    assert result["overall_conclusion"] == "likely stationary"
    assert result["adf"]["conclusion"] == "stationary"
    assert result["kpss"]["conclusion"] == "stationary"


def test_stationarity_tests_handles_short_series() -> None:
    result = diagnostics.stationarity_tests(pd.Series([1.0, 2.0, np.nan]))

    assert result["overall_conclusion"] == "insufficient data"
    assert result["adf"]["conclusion"] == "not run"
    assert result["kpss"]["conclusion"] == "not run"


def test_stationarity_tests_rejects_invalid_kpss_regression() -> None:
    try:
        diagnostics.stationarity_tests(pd.Series(np.arange(12.0)), kpss_regression="x")
    except ValueError as exc:
        assert "kpss_regression" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
