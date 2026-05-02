from __future__ import annotations

import pandas as pd
import pytest

from baci_climate_index.composite import (
    build_baci,
    orient_drought,
    require_complete_components,
)


def _components() -> pd.DataFrame:
    index = pd.period_range("1961-01", "1961-03", freq="M").to_timestamp("M")
    return pd.DataFrame(
        {
            "precipitation": [1.0, 2.0, 3.0],
            "t90": [2.0, 2.0, 2.0],
            "t10": [1.0, 1.0, 1.0],
            "drought": [0.0, 1.0, 2.0],
            "wind": [1.0, 1.0, 1.0],
            "sealevel": [3.0, 3.0, 3.0],
        },
        index=index,
    )


def test_build_baci_uses_final_formula() -> None:
    result = build_baci(_components())

    expected = pd.Series(
        [(2 - 1 + 1 + 0 + 3 + 1) / 6, (2 - 1 + 2 + 1 + 3 + 1) / 6, (2 - 1 + 3 + 2 + 3 + 1) / 6],
        index=_components().index,
        name="BACI",
    )
    pd.testing.assert_series_equal(result, expected)


def test_build_baci_allows_sealevel_weight_sensitivity() -> None:
    result = build_baci(_components(), sealevel_weight=2.0)

    assert result.iloc[0] == pytest.approx((2 - 1 + 1 + 0 + 6 + 1) / 6)


def test_orient_drought_flips_spi_like_input() -> None:
    components = _components()
    oriented = orient_drought(components, drought_is_spi=True)

    assert oriented["drought"].tolist() == [0.0, -1.0, -2.0]
    assert components["drought"].tolist() == [0.0, 1.0, 2.0]


def test_require_complete_components_raises_on_missing_values() -> None:
    components = _components()
    components.loc[components.index[0], "t90"] = None

    with pytest.raises(ValueError, match="Unexpected missing"):
        require_complete_components(components)
