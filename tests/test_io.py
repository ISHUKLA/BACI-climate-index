from __future__ import annotations

import pandas as pd
import xarray as xr

from baci_climate_index.io import collapse_to_monthly_series, load_component_series, monthly_index


def test_monthly_index_uses_month_end_timestamps() -> None:
    index = monthly_index("1961-01", "1961-03")

    assert index.tolist() == [
        pd.Timestamp("1961-01-31"),
        pd.Timestamp("1961-02-28"),
        pd.Timestamp("1961-03-31"),
    ]


def test_collapse_to_monthly_series_averages_non_time_dimensions() -> None:
    full_index = monthly_index("1961-01", "1961-02")
    data_array = xr.DataArray(
        [[1.0, 3.0], [2.0, 4.0]],
        coords={
            "time": [pd.Timestamp("1961-01-01"), pd.Timestamp("1961-02-01")],
            "step": [1, 2],
        },
        dims=("time", "step"),
    )

    result = collapse_to_monthly_series(data_array, full_index=full_index, name="example")

    assert result.name == "example"
    assert result.index.tolist() == full_index.tolist()
    assert result.tolist() == [2.0, 3.0]


def test_load_sealevel_averages_multiple_station_variables(tmp_path) -> None:
    full_index = monthly_index("1961-01", "1961-02")
    dataset = xr.Dataset(
        {
            "Measurement_470": ("time", [1.0, 3.0]),
            "Measurement_489": ("time", [3.0, 5.0]),
        },
        coords={"time": [pd.Timestamp("1961-01-01"), pd.Timestamp("1961-02-01")]},
    )
    path = tmp_path / "sealevel_index.nc"
    dataset.to_netcdf(path)

    result = load_component_series("sealevel", path, full_index=full_index)

    assert result.tolist() == [2.0, 4.0]
