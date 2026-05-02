"""I/O helpers for BACI component series."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import xarray as xr


def monthly_index(start_month: str, end_month: str) -> pd.DatetimeIndex:
    """Return a month-end datetime index covering the requested period."""
    return pd.period_range(start_month, end_month, freq="M").to_timestamp("M")


def collapse_to_monthly_series(
    data_array: xr.DataArray,
    *,
    full_index: pd.DatetimeIndex,
    name: str,
) -> pd.Series:
    """Collapse any non-time dimensions and align the series to a monthly grid."""
    time_dim = "time" if "time" in data_array.dims else data_array.dims[0]
    other_dims = [dim for dim in data_array.dims if dim != time_dim]

    if other_dims:
        data_array = data_array.mean(dim=other_dims, skipna=True)

    series = data_array.to_series()
    series.index = pd.to_datetime(series.index).to_period("M").to_timestamp("M")
    series = series.reindex(full_index)
    series.name = name
    return series


def load_component_series(
    name: str,
    path: str | Path,
    *,
    full_index: pd.DatetimeIndex,
) -> pd.Series:
    """Load a component NetCDF file as a 1-D monthly pandas series."""
    component_path = Path(path)
    if not component_path.exists():
        raise FileNotFoundError(f"Missing component file for {name}: {component_path}")

    with xr.open_dataset(component_path) as dataset:
        if name == "sealevel":
            data_array = _load_sealevel(dataset)
        elif name in dataset.data_vars:
            data_array = dataset[name]
        elif f"{name}_index" in dataset.data_vars:
            data_array = dataset[f"{name}_index"]
        elif len(dataset.data_vars) == 1:
            data_array = next(iter(dataset.data_vars.values()))
        else:
            names = ", ".join(dataset.data_vars)
            raise ValueError(
                f"Could not identify variable for {name} in {component_path}. "
                f"Available variables: {names}"
            )

        return collapse_to_monthly_series(data_array, full_index=full_index, name=name)


def load_components(
    component_paths: dict[str, Path],
    *,
    full_index: pd.DatetimeIndex,
) -> pd.DataFrame:
    """Load all configured component files into one aligned DataFrame."""
    series = {
        name: load_component_series(name, path, full_index=full_index)
        for name, path in component_paths.items()
    }
    return pd.DataFrame(series, index=full_index)


def save_baci_netcdf(series: pd.Series, output_path: str | Path) -> Path:
    """Save BACI as a compressed NetCDF file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    data_array = xr.DataArray(
        series.to_numpy(),
        coords={"time": series.index},
        dims="time",
        name="BACI",
    )
    dataset = xr.Dataset({"BACI": data_array})
    encoding = {"BACI": {"zlib": True, "complevel": 4, "dtype": "float32"}}

    tmp_path = output.with_suffix(output.suffix + ".tmp")
    dataset.to_netcdf(tmp_path, engine="netcdf4", encoding=encoding)
    tmp_path.replace(output)
    return output


def _load_sealevel(dataset: xr.Dataset) -> xr.DataArray:
    if "sealevel_index" in dataset.data_vars:
        return dataset["sealevel_index"]
    return dataset.to_array().mean(dim="variable", skipna=True)
