# Data Sources

The final calibration uses open climate data from two primary sources.

## Primary Sources

ERA5-Land reanalysis is available from the Copernicus Climate Data Store:

https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview

Permanent Service for Mean Sea Level data is available from PSMSL:

https://psmsl.org/data/obtaining/

## Prepared Input Bundle

For reproducibility of this project, the prepared input bundle used during
calibration is stored in this Google Drive folder:

https://drive.google.com/drive/folders/1felOqtKFJkbyaA68T0-ZnsR2uYJl6R5o

### Folder Contents

```text
era5_land_data/
PSMSL/
documentation_aci.pdf
```

## ERA5-Land Usage

The `era5_land_data` folder contains monthly GRIB files following this naming
pattern:

```text
era5_land_YYYY_MM.grib
```

These files are derived from ERA5-Land and are used upstream to derive the
precipitation, temperature, drought, and wind component indices.

## PSMSL Usage

The `PSMSL` folder contains:

```text
rlr_monthly.zip
```

This archive is derived from PSMSL monthly revised local reference data and is
used upstream to derive the sea-level component index.

## Repository Policy

Raw data is not committed to Git because it is large and can be refreshed from
the source folder. Generated component files should be produced locally and
referenced through `configs/default.yaml`.

The composite builder expects these generated NetCDF component files:

```text
precipitation_index.nc
t90_index.nc
t10_index.nc
drought_index.nc
wind_index.nc
sealevel_index.nc
```
