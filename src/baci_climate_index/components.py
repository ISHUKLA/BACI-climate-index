"""Thin wrappers for upstream ACI component calculations.

These helpers keep the GitHub-facing code readable while still allowing the
existing upstream `aci.components` implementation to do the heavy climate-index
calculation. They are intentionally optional: the composite builder only needs
the generated component NetCDF files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from dask.diagnostics import ProgressBar


class AreaComponent(Protocol):
    """Protocol for the upstream ACI component API."""

    def calculate_component(self, *, reference_period: tuple[str, str], area: bool):
        """Return a lazy or eager component index."""


def compute_area_component(
    component: AreaComponent,
    *,
    reference_period: tuple[str, str],
    output_path: str | Path,
    start_date: str = "1961-01-01",
) -> Path:
    """Compute an area-mean component and write it to NetCDF."""
    index = component.calculate_component(reference_period=reference_period, area=True)
    with ProgressBar():
        computed = index.compute() if hasattr(index, "compute") else index

    cleaned = computed.sel(time=slice(start_date, None))
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_netcdf(output)
    return output
