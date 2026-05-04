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

Create and activate an environment, then install the project. With `venv`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

Or with Conda/Mamba:

```bash
mamba env create -f environment.yml
conda activate baci-climate-index
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
ruff check .
```

## Data

Large raw data and generated NetCDF files are intentionally excluded from Git.
Set the paths in `configs/default.yaml` to point at your local data directory.

Primary data sources:

- ERA5-Land reanalysis from the Copernicus Climate Data Store:
  https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview
- Permanent Service for Mean Sea Level data:
  https://psmsl.org/data/obtaining/

### Extracted Data Description

**Data Sources**

ERA5-Land, from Copernicus, provides climate reanalysis data at a spatial
resolution around 0.1 degrees, approximately 11 km.

PSMSL, the Permanent Service for Mean Sea Level, provides tide-gauge sea-level
data from three Belgian coastal stations:

- Nieuwpoort
- Oostende
- Zeebrugge

**Period**

The slides mention a long homogeneous period from around 1961-2023. Elsewhere
in the project pipeline and results, the analysis period is 1961-2024. The
reference and normalisation period is 1961-1990.

**Coverage**

ERA5-Land covers the Belgian territory with around 250 grid cells. A geographic
Belgian mask is applied to exclude grid cells outside Belgium.

**Variables Used**

The data are used to derive climate components for:

- precipitation
- temperature extremes
- drought
- wind
- sea level

**Data Quality**

ERA5-Land is described as a reference climate reanalysis from ECMWF, combining
observations and physical models. PSMSL is described as an internationally
validated sea-level database. The slides emphasize long, homogeneous time
series.

**Cleaning and Harmonisation**

The cleaning workflow applies a geographic mask so cells outside Belgium are
removed. Missing sea-level data are handled using an inter-station average
across the PSMSL stations. ERA5-Land gaps/interpolation are mentioned in the
slide extraction, although the extracted text is partially fragmented. All
variables are converted to comparable z-scores relative to 1961-1990.

**Limitations**

ERA5-Land resolution of 0.1 degrees, or approximately 11 km, may be coarse for
a compact country like Belgium. Local gradients may be smoothed, especially:

- urban effects
- coastal effects
- relief/topography

Reliable historical series start around 1961. Updates depend on data
publication schedules from Copernicus and PSMSL.

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

The final results correspond to `notebooks/index_VF.ipynb` and the Keynote deck
`Actuarial index calibration - Open source Belgian data.key`.

## Citation and reuse

This repository is released under the MIT License. Citation metadata is provided
in `CITATION.cff`, which GitHub can render as a suggested citation.

For an archived, citable release:

1. Create a GitHub release from a version tag, for example `v0.1.0`.
2. Enable the repository in Zenodo's GitHub integration before publishing the
   release.
3. After Zenodo archives the release, copy the DOI into this README and update
   `CITATION.cff` with the DOI.
