# Data Sources

The final calibration uses the dataset folder:

https://drive.google.com/drive/folders/1felOqtKFJkbyaA68T0-ZnsR2uYJl6R5o

## Folder Contents

```text
era5_land_data/
PSMSL/
documentation_aci.pdf
```

## ERA5-Land

The `era5_land_data` folder contains monthly GRIB files following this naming
pattern:

```text
era5_land_YYYY_MM.grib
```

These files are used upstream to derive the precipitation, temperature, drought,
and wind component indices.

## PSMSL

The `PSMSL` folder contains:

```text
rlr_monthly.zip
```

This archive is used upstream to derive the sea-level component index.

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
