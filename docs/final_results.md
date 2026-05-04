# Results Reference

The values below came from the earlier six-component calibration preserved for
provenance. They should be regenerated before publication under the current
five-component methodology:

```text
BACI = (t90 - t10 + precipitation + wind + 0.35 * sealevel) / 5
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
