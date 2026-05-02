# BACI Climate Index

This repository contains the cleaned, reproducible code used to build the Belgian
Actuarial Climate Index (BACI) from open climate data.

The original exploratory work lives in `notebooks/`. The production path is the
Python package in `src/baci_climate_index`, which loads the component NetCDF
files, aligns them to a monthly grid, validates reference-period standardisation,
builds the BACI composite, and writes final outputs.

## Final BACI formula

The final composite is:

```text
BACI = (t90 - t10 + precipitation + drought + sealevel + wind) / 6
```

where all six inputs are standardised monthly component indices over the
1961-1990 reference period.

## Final result sanity check

The final notebook and presentation show:

```text
BACI min:  -1.462
BACI max:   2.203
BACI mean:  0.274
BACI std:   0.584
BACI NaNs:  0
```

## Repository layout

```text
configs/                  Configuration files
docs/                     Notes on methodology and data handling
notebooks/                Original notebooks kept for provenance
src/baci_climate_index/   Reusable Python package
tests/                    Unit tests for core BACI logic
```

## Quick start

Create and activate an environment, then install the project:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

Build the composite from the configured component files:

```bash
baci build-composite --config configs/default.yaml
```

Show diagnostics for a generated BACI file:

```bash
baci describe outputs/BACI_composite.nc
```

Run tests:

```bash
pytest
```

## Data

Large raw data and generated NetCDF files are intentionally excluded from Git.
Set the paths in `configs/default.yaml` to point at your local data directory.

The source dataset used for the final calibration is stored here:

https://drive.google.com/drive/folders/1felOqtKFJkbyaA68T0-ZnsR2uYJl6R5o

It contains:

```text
era5_land_data/       Monthly ERA5-Land GRIB files, e.g. era5_land_2024_12.grib
PSMSL/                Permanent Service for Mean Sea Level data, rlr_monthly.zip
documentation_aci.pdf Supporting project documentation
```

Expected component files:

```text
precipitation_index.nc
t90_index.nc
t10_index.nc
drought_index.nc
wind_index.nc
sealevel_index.nc
```

## Provenance

The final results correspond to `index_VF (5).ipynb` and the Keynote deck
`Actuarial index calibration - Open source Belgian data.key`.
