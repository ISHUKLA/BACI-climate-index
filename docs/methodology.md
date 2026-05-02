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
t90 - t10 + precipitation + drought + sealevel + wind
```

The `t10` term is subtracted so that decreasing cold-tail values contribute to
an increasing climate-risk signal. The final drought component is already
oriented so that higher values represent drier conditions. If using an SPI-like
drought input where positive means wetter, set `drought_is_spi: true` in the
configuration to flip the sign.

## Missing Values

The final workflow requires no missing values across component series. This is
intentional: missing component months should be fixed upstream, not silently
dropped in the composite.
