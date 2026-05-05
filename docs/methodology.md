# Methodology Notes

## Reference Period

All component indices are standardised against the 1961-1990 reference period.
Before the composite is built, the code checks that component means are close to
zero and standard deviations are close to one over this period.

## Monthly Alignment

All inputs are normalised to month-end timestamps and reindexed to the full
monthly grid from January 1961 through December 2024. This avoids silent
off-by-one month shifts when mixing pandas and xarray outputs.

## Component Selection And Direction

The final BACI formula keeps five components:

```text
BACI = (t90 - t10 + precipitation + wind + fS * sealevel) / 5
fS = 0.024
```

The `t10` term is subtracted so that decreasing cold-tail values contribute to
an increasing climate-risk signal. Precipitation, hot extremes, wind, and sea
level are added so that positive anomalies increase the index.

Wind is retained in the production BACI despite the older slide-14 statement
that it was dropped. The retained-code decision is supported by the same
validation logic used for the drought exclusion: wind has a contemporaneous
component-BACI correlation of `0.478`, passes the AR(1)-adjusted FDR lag screen
at lag 0 with `p = 0.000`, and represents an ACI/FACI climate dimension that is
not redundant with drought. Dropping wind would remove a statistically visible
hazard signal and would leave the production formula inconsistent with the
validated five-dimension composite. The current methodology therefore treats
the slide-14 dropped-wind text as superseded by the retained production
specification.

Drought is excluded from the final BACI after validation showed weak marginal
contribution in Belgium. It can remain in exploratory notebooks or diagnostics,
but the production composite ignores drought even if a drought column is present
in the input frame.

Sea level is multiplied by `fS = 0.024` to avoid overweighting a geographically
limited coastal exposure in the national index. The denominator remains fixed at
`5`, matching the five retained climate dimensions rather than the weighted sum
of numerator coefficients.

The Shapley/LMG contribution check is preserved in
`notebooks/index_VF_stats.ipynb`; use that notebook when revisiting component
selection or explaining the drought exclusion.

## Missing Values

The final workflow requires no missing values across component series. This is
intentional: missing component months should be fixed upstream, not silently
dropped in the composite.
