"""Command-line interface for BACI workflows."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import xarray as xr

from baci_climate_index.composite import (
    build_baci,
    component_correlations,
    decadal_means,
    reference_summary,
    require_complete_components,
    sealevel_fs_sensitivity,
    summary_stats,
    write_fingerprint,
)
from baci_climate_index.config import load_config
from baci_climate_index.diagnostics import event_frequency, linear_trend_per_decade
from baci_climate_index.io import load_components, monthly_index, save_baci_netcdf
from baci_climate_index.plotting import save_decadal_bar_chart


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="baci")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build-composite", help="Build BACI NetCDF output")
    build_parser.add_argument("--config", default="configs/default.yaml", help="YAML config path")

    describe_parser = subparsers.add_parser("describe", help="Describe a BACI NetCDF file")
    describe_parser.add_argument("path", help="Path to BACI_composite.nc")

    args = parser.parse_args(argv)

    if args.command == "build-composite":
        return _build_composite(Path(args.config))
    if args.command == "describe":
        return _describe(Path(args.path))

    parser.error(f"Unknown command: {args.command}")
    return 2


def _build_composite(config_path: Path) -> int:
    config = load_config(config_path)
    full_index = monthly_index(config.study.start_month, config.study.end_month)

    components = load_components(config.component_paths, full_index=full_index)

    if config.options.require_no_missing:
        require_complete_components(components)

    print("\nReference-period sanity check:")
    print(
        reference_summary(
            components,
            reference_start=config.study.reference_start,
            reference_end=config.study.reference_end,
        )
        .round(3)
        .to_string()
    )

    baci = build_baci(components, fs=config.fs)
    frame = components.assign(BACI=baci)

    print("\nBACI summary:")
    for key, value in summary_stats(baci).items():
        print(f"{key}: {value:.3f}" if isinstance(value, float) else f"{key}: {value}")

    print("\nCorrelation matrix:")
    print(component_correlations(frame).round(3).to_string())

    print("\nComponent-BACI correlations:")
    print(component_correlations(frame)["BACI"].drop("BACI").sort_values(ascending=False).round(3))

    print("\nDecadal BACI means:")
    print(decadal_means(baci).round(3).to_string())

    print("\nSea-level fS sensitivity:")
    print(sealevel_fs_sensitivity(components, base_fs=config.fs).round(3))

    output_nc = config.paths.output_dir / "BACI_composite.nc"
    save_baci_netcdf(baci, output_nc)
    print(f"\nSaved NetCDF: {output_nc}")

    if config.options.make_decadal_png:
        output_png = config.paths.output_dir / "BACI_decadal_means.png"
        save_decadal_bar_chart(baci, output_png)
        print(f"Saved PNG: {output_png}")

    fingerprint_path = config.paths.output_dir / "BACI_fingerprint.json"
    print(f"Fingerprint: {write_fingerprint(baci, fingerprint_path)}")
    return 0


def _describe(path: Path) -> int:
    with xr.open_dataset(path) as dataset:
        if "BACI" not in dataset:
            raise ValueError(f"Expected variable 'BACI' in {path}")
        series = dataset["BACI"].to_series()

    series.index = pd.to_datetime(series.index).to_period("M").to_timestamp("M")

    print("BACI summary:")
    for key, value in summary_stats(series).items():
        print(f"{key}: {value:.3f}" if isinstance(value, float) else f"{key}: {value}")

    print("\nEvent frequency:")
    print(event_frequency(series))

    print("\nLinear trend:")
    print(linear_trend_per_decade(series))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
