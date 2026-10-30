# 3. Summary statistics

Table 1 describes the two 30-year periods we compare, 1961-1990 (early) and
1996-2025 (recent), by index and country. For TXx we pool June, July and
August and express each value as an anomaly: its difference, in °C, from the
1961-1990 mean of the same month in the same country. Table 2 gives these
reference levels. Without this step the pooled distribution would mix three
seasonal levels; in Spain, for instance, the July reference (33.31 °C) is more
than 3 °C above the June one (30.14 °C). With anomalies the three months share
one scale, each country contributes 90 observations per period, and the
early-period mean is zero by construction. SPEI-6 is used as published, one
September value per year, giving 30 observations per country and period. The
years 1950-1960 and 1991-1995 belong to neither period: they enter the trends
of Section 5 but not this table. Percentiles are computed by linear
interpolation between ordered values.

**Table 1.** Summary statistics by index, country and period.

| Index | Country | Period | N | Mean | SD | Min | P5 | P25 | Median | P75 | P95 | Max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TXx | ESP | 1961-1990 | 90 | 0.00 | 1.61 | -5.05 | -2.86 | -0.84 | 0.00 | 1.12 | 2.03 | 4.06 |
| TXx | ESP | 1996-2025 | 90 | 2.10 | 1.74 | -2.16 | -0.69 | 1.04 | 1.98 | 3.05 | 5.31 | 5.89 |
| TXx | FRA | 1961-1990 | 90 | 0.00 | 1.83 | -3.57 | -2.73 | -1.32 | -0.14 | 1.28 | 3.16 | 4.27 |
| TXx | FRA | 1996-2025 | 90 | 2.44 | 2.35 | -4.04 | -1.02 | 0.87 | 2.34 | 3.92 | 6.35 | 8.21 |
| TXx | GER | 1961-1990 | 90 | 0.00 | 1.78 | -4.63 | -2.95 | -1.21 | -0.03 | 1.27 | 2.89 | 4.01 |
| TXx | GER | 1996-2025 | 90 | 1.85 | 2.37 | -4.12 | -1.91 | 0.51 | 1.98 | 3.80 | 5.29 | 6.74 |
| TXx | SWE | 1961-1990 | 90 | 0.00 | 2.06 | -4.85 | -3.76 | -1.23 | 0.01 | 1.53 | 3.18 | 4.61 |
| TXx | SWE | 1996-2025 | 90 | 0.63 | 2.15 | -4.45 | -2.76 | -0.98 | 0.74 | 2.17 | 4.18 | 4.98 |
| SPEI-6 | ESP | 1961-1990 | 30 | 0.15 | 0.75 | -1.02 | -0.89 | -0.34 | 0.09 | 0.46 | 1.44 | 2.30 |
| SPEI-6 | ESP | 1996-2025 | 30 | -0.62 | 0.70 | -1.82 | -1.63 | -1.11 | -0.69 | -0.17 | 0.59 | 0.80 |
| SPEI-6 | FRA | 1961-1990 | 30 | 0.05 | 0.86 | -1.70 | -1.40 | -0.41 | 0.19 | 0.66 | 1.15 | 1.25 |
| SPEI-6 | FRA | 1996-2025 | 30 | -0.56 | 0.77 | -1.98 | -1.56 | -1.12 | -0.75 | 0.23 | 0.41 | 0.85 |
| SPEI-6 | GER | 1961-1990 | 30 | 0.21 | 0.82 | -1.90 | -1.04 | -0.35 | 0.42 | 0.76 | 1.31 | 1.70 |
| SPEI-6 | GER | 1996-2025 | 30 | -0.36 | 0.91 | -2.80 | -1.95 | -0.85 | -0.30 | 0.39 | 0.82 | 0.97 |
| SPEI-6 | SWE | 1961-1990 | 30 | -0.10 | 0.68 | -1.99 | -1.27 | -0.41 | -0.03 | 0.20 | 0.99 | 1.26 |
| SPEI-6 | SWE | 1996-2025 | 30 | 0.07 | 0.80 | -1.89 | -1.15 | -0.38 | -0.01 | 0.50 | 1.42 | 1.56 |

*TXx: anomaly in °C from the 1961-1990 mean of the same country and month
(Table 2), June-August pooled. SPEI-6: September value, dimensionless;
negative means drier than the 1971-2005 reference climate. P5 and P95: 5th and
95th percentiles. Source: Copernicus Interactive Climate Atlas v2.5, ERA5-Land,
accessed 29 October 2026; our calculations (`scripts/analysis.py`, full table
including 1950-2025 in `outputs/summary_stats.csv`).*

**Table 2.** TXx reference levels: 1961-1990 mean, °C.

| Country | June | July | August |
|---|---|---|---|
| ESP | 30.14 | 33.31 | 32.90 |
| FRA | 26.85 | 29.59 | 28.97 |
| GER | 26.86 | 28.29 | 28.19 |
| SWE | 23.27 | 24.06 | 22.27 |

*Mean over 1961-1990 of the monthly maximum of daily maximum temperature,
country average. Source: as Table 1 (`outputs/txx_baseline.csv`).*

Summer maximum temperatures are higher in the recent period in all four
countries. The mean anomaly is 2.44 °C in France, 2.10 °C in Spain, 1.85 °C in
Germany and 0.63 °C in Sweden. The whole distribution moved up, the cool end
included: the 5th percentile rose from -2.86 to -0.69 °C in Spain and from
-2.73 to -1.02 °C in France. The top moved further than the mean in every
country: the 95th percentile went from 2.03 to 5.31 °C in Spain, from 3.16 to
6.35 °C in France, from 2.89 to 5.29 °C in Germany and from 3.18 to 4.18 °C in
Sweden. In France and Germany the spread also widened, the standard deviation
rising from 1.83 to 2.35 °C and from 1.78 to 2.37 °C, while it changed little
in Spain (1.61 to 1.74 °C) and Sweden (2.06 to 2.15 °C). Read at face value,
the table shows a shift of the whole distribution with a larger rise at the
top; Section 5 asks whether that extra rise exceeds sampling noise.

For SPEI-6, the April-September water balance became drier on average in
Spain, France and Germany: the mean fell from 0.15 to -0.62 in Spain, from 0.05
to -0.56 in France and from 0.21 to -0.36 in Germany. In Sweden it changed
little, from -0.10 to 0.07. The dry tail followed the mean in Spain and
Germany, where the 5th percentile fell from -0.89 to -1.63 and from -1.04 to
-1.95, but moved much less in France (-1.40 to -1.56). Germany has the driest
value of the comparison, -2.80, in the recent period. The spread of SPEI-6
stayed within 0.68 to 0.91 in every country and period.

These tail statistics rest on few observations. With 90 pooled TXx values, the
95th percentile lies between the 85th and 86th ordered values, so only five
observations lie above it in each period; with 30 SPEI-6 values, the 5th
percentile lies between the second and third lowest, so only two lie below
it. The TXx observations are not independent events either, because the three
months of a summer tend to be hot together: the five values above the recent
95th percentile come from five distinct summers in Spain, four in Germany and
Sweden, and only three in France (`outputs/shift_shape.csv`). At the most
extreme thresholds used in Section 5, the 99th percentile of TXx and the 1st
of SPEI-6, a single early-period observation lies beyond the line in each
country (`outputs/exceedance.csv`). A gap between two tail percentiles in
Table 1 can therefore be driven by one or two exceptional years, which is why
Section 5 reports bootstrap confidence intervals that resample whole years
rather than single months.
