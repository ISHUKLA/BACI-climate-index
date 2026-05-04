# Methodology Notes

## Reference Period

All component indices are standardised against the 1961-1990 reference period.
Before the composite is built, the code checks that component means are close to
zero and standard deviations are close to one over this period.

## Monthly Alignment

All inputs are normalised to month-end timestamps and reindexed to the full
monthly grid from January 1961 through December 2024. This avoids silent
off-by-one month shifts when mixing pandas and xarray outputs.

## Component Direction

The final BACI formula uses:

```text
BACI = (t90 - t10 + precipitation + wind + 0.35 * sealevel) / 5
```

The `t10` term is subtracted so that decreasing cold-tail values contribute to
an increasing climate-risk signal. Wind remains included in the final composite.
Drought is excluded from the final BACI after validation showed weak marginal
contribution in Belgium. Sea level is multiplied by `fS = 0.35` to avoid
overweighting a geographically limited coastal exposure.

## Missing Values

The final workflow requires no missing values across component series. This is
intentional: missing component months should be fixed upstream, not silently
dropped in the composite.
