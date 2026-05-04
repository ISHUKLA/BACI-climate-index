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

## Extracted Data Description From Slides

### Data Sources

ERA5-Land, from Copernicus, provides climate reanalysis data at a spatial
resolution around 0.1 degrees, approximately 11 km.

PSMSL, the Permanent Service for Mean Sea Level, provides tide-gauge sea-level
data from three Belgian coastal stations:

- Nieuwpoort
- Oostende
- Zeebrugge

### Period

The slides mention a long homogeneous period from around 1961-2023. Elsewhere
in the project pipeline and results, the analysis period is 1961-2024. The
reference and normalisation period is 1961-1990.

### Coverage

ERA5-Land covers the Belgian territory with around 250 grid cells. A geographic
Belgian mask is applied to exclude grid cells outside Belgium.

### Variables Used

The data are used to derive climate components for:

- precipitation
- temperature extremes
- drought
- wind
- sea level

### Data Quality

ERA5-Land is described as a reference climate reanalysis from ECMWF, combining
observations and physical models. PSMSL is described as an internationally
validated sea-level database. The slides emphasize long, homogeneous time
series.

### Cleaning and Harmonisation

The cleaning workflow applies a geographic mask so cells outside Belgium are
removed. Missing sea-level data are handled using an inter-station average
across the PSMSL stations. ERA5-Land gaps/interpolation are mentioned in the
slide extraction, although the extracted text is partially fragmented. All
variables are converted to comparable z-scores relative to 1961-1990.

### Limitations

ERA5-Land resolution of 0.1 degrees, or approximately 11 km, may be coarse for
a compact country like Belgium. Local gradients may be smoothed, especially:

- urban effects
- coastal effects
- relief/topography

Reliable historical series start around 1961. Updates depend on data
publication schedules from Copernicus and PSMSL.

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
