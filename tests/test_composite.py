from __future__ import annotations

import pandas as pd
import pytest

from baci_climate_index.composite import (
    DEFAULT_SEALEVEL_FS,
    build_baci,
    require_complete_components,
    smooth_5yr,
    to_quarterly,
)


def _components() -> pd.DataFrame:
    index = pd.period_range("1961-01", "1961-03", freq="M").to_timestamp("M")
    return pd.DataFrame(
        {
            "precipitation": [1.0, 2.0, 3.0],
            "t90": [2.0, 2.0, 2.0],
            "t10": [1.0, 1.0, 1.0],
            "wind": [1.0, 1.0, 1.0],
            "sealevel": [3.0, 3.0, 3.0],
        },
        index=index,
    )


class TestBuildBaci:
    def test_build_baci_uses_final_formula(self) -> None:
        components = _components()
        result = build_baci(components, fs=0.024)

        expected = pd.Series(
            [
                (2 - 1 + 1 + 1 + 0.024 * 3) / 5,
                (2 - 1 + 2 + 1 + 0.024 * 3) / 5,
                (2 - 1 + 3 + 1 + 0.024 * 3) / 5,
            ],
            index=components.index,
            name="BACI",
        )
        pd.testing.assert_series_equal(result, expected, check_freq=False)

    def test_build_baci_defaults_to_public_fs(self) -> None:
        pd.testing.assert_series_equal(
            build_baci(_components()),
            build_baci(_components(), fs=DEFAULT_SEALEVEL_FS),
        )

    def test_build_baci_allows_custom_fs(self) -> None:
        result = build_baci(_components(), fs=2.0)

        assert result.iloc[0] == pytest.approx((2 - 1 + 1 + 1 + 2.0 * 3) / 5)

    def test_build_baci_allows_zero_fs(self) -> None:
        result = build_baci(_components(), fs=0.0)

        assert result.iloc[0] == pytest.approx((2 - 1 + 1 + 1) / 5)

    def test_build_baci_names_series(self) -> None:
        assert build_baci(_components()).name == "BACI"

    def test_build_baci_raises_on_missing_component_column(self) -> None:
        components = _components().drop(columns=["wind"])

        with pytest.raises(ValueError, match="Missing BACI component columns"):
            build_baci(components)

    def test_drought_column_ignored_if_present(self) -> None:
        components = _components()
        with_drought = components.assign(drought=[-999.0, None, 999.0])

        pd.testing.assert_series_equal(build_baci(components), build_baci(with_drought))
        require_complete_components(with_drought)


class TestRequireCompleteComponents:
    def test_require_complete_components_accepts_complete_frame(self) -> None:
        require_complete_components(_components())

    def test_require_complete_components_raises_on_missing_values(self) -> None:
        components = _components()
        components.loc[components.index[0], "t90"] = None

        with pytest.raises(ValueError, match="Unexpected missing"):
            require_complete_components(components)


class TestTemporalHelpers:
    def test_to_quarterly_returns_quarter_end_means(self) -> None:
        index = pd.period_range("2020-01", "2020-06", freq="M").to_timestamp("M")
        series = pd.Series([1, 2, 3, 4, 5, 6], index=index, name="BACI")

        result = to_quarterly(series)

        expected = pd.Series(
            [2.0, 5.0],
            index=pd.to_datetime(["2020-03-31", "2020-06-30"]),
            name="BACI",
        )
        pd.testing.assert_series_equal(result, expected, check_freq=False)

    def test_to_quarterly_preserves_name(self) -> None:
        series = pd.Series(
            [1.0, 2.0, 3.0],
            index=pd.period_range("2020-01", "2020-03", freq="M").to_timestamp("M"),
            name="example",
        )

        assert to_quarterly(series).name == "example"

    def test_smooth_5yr_uses_centered_60_month_window(self) -> None:
        index = pd.period_range("2000-01", "2004-12", freq="M").to_timestamp("M")
        series = pd.Series(range(60), index=index, name="BACI")

        result = smooth_5yr(series)

        assert result.iloc[30] == pytest.approx(29.5)
        assert result.dropna().shape[0] == 1

    def test_smooth_5yr_preserves_name(self) -> None:
        index = pd.period_range("2000-01", "2004-12", freq="M").to_timestamp("M")
        series = pd.Series(range(60), index=index, name="example")

        assert smooth_5yr(series).name == "example"
