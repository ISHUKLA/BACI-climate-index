# Results Reference

The values below are preserved for provenance from the earlier calibration.
They should be regenerated before publication under the current five-component
methodology:

```text
BACI = (t90 - t10 + precipitation + wind + fS * sealevel) / 5
fS = 0.024
```

The earlier results were taken from the Keynote deck:

```text
Actuarial index calibration - Open source Belgian data.key
```

The source notebook preserved for those results is:

```text
notebooks/index_VF.ipynb
```

## BACI Summary

```text
min:        -1.462
max:         2.203
mean:        0.274
std:         0.584
count NaNs:  0
```

## Component-BACI Correlations

```text
sealevel         0.726
t90              0.698
wind             0.478
precipitation    0.433
drought          0.044
t10             -0.707
```

## Decadal BACI Means

```text
1960s   -0.132
1970s   -0.097
1980s    0.160
1990s    0.375
2000s    0.481
2010s    0.493
2020s    0.919
```

## Presentation Chart Values

```text
BACI trend: +0.162 sigma/decade
BACI study-period mean shift vs reference: +0.52
Moderate BACI months, 1 sigma < |x| <= 2 sigma: 92 months
Extreme BACI months, |x| > 2 sigma: 2 months
```

## Empirical Extreme-Event Counts

The Gaussian two-sigma count is intentionally strict and low: it assumes the
standard-normal tail is the relevant definition of "extreme" after
standardisation. For communication, the empirical quantile view is often easier
to interpret because it asks how many months sit in the observed upper tail of
the BACI distribution.

The historical series contains 768 monthly observations. Empirical exceedance
counts are therefore:

| Definition | Share of months | Count |
| --- | ---: | ---: |
| Empirical Q80 exceedance | Top 20% | 154 months |
| Empirical Q95 exceedance | Top 5% | 39 months |

These quantile counts are distribution-free and should be reported alongside,
not instead of, the Gaussian one- and two-sigma diagnostics.

## Stationarity Note

Stationarity diagnostics were run on the generated BACI series in
`/Users/coralieroland/ACI-Python/data/composites/BACI_composite.nc` using
`stationarity_tests()` with `kpss_regression="c"`:

| Test | Null hypothesis | p-value | Interpretation at alpha = 0.05 |
| --- | --- | ---: | --- |
| ADF | Unit root / non-stationary | 0.0261 | Reject non-stationarity |
| KPSS | Level-stationary | 0.0100 | Reject stationarity |

The KPSS p-value is the lower table bound reported by `statsmodels`; the test
warning indicates that the actual p-value is smaller. Taken together, ADF and
KPSS give mixed evidence: the BACI series is standardised against the 1961-1990
reference period, but the full 1961-2024 series still carries a long-run climate
signal and should not be treated as distributionally stable.
