# 5. Econometrics

## 5.1. Fixed thresholds and a shift benchmark

We set each country's thresholds on 1961-1990 and apply the same values to
1996-2025. Frequency is the share of observations above the TXx threshold or
below the SPEI-6 threshold, not a count of distinct heatwaves or drought
episodes. Let delta = mean_recent - mean_early. The shift benchmark adds delta
to every early observation and recounts exceedances. It preserves the early
distribution's shape and uses the observed mean change; it is a descriptive
benchmark, not an independent forecast.

**Table 3. Threshold sensitivity: early count / recent count / shift-benchmark
count.**

| Index | Country | P75 / P25 | P90 / P10 | P95 / P5 | P99 / P1 |
|---|---|---|---|---|---|
| TXx | Spain | 23 / 65 / 70 | 9 / 47 / 54 | 5 / 43 / 48 | 1 / 14 / 11 |
| TXx | France | 23 / 62 / 64 | 9 / 44 / 42 | 5 / 27 / 29 | 1 / 20 / 16 |
| TXx | Germany | 23 / 55 / 56 | 9 / 41 / 37 | 5 / 31 / 27 | 1 / 24 / 14 |
| TXx | Sweden | 23 / 36 / 30 | 9 / 18 / 13 | 5 / 9 / 9 | 1 / 3 / 3 |
| SPEI-6 | Spain | 8 / 20 / 21 | 3 / 16 / 15 | 2 / 12 / 11 | 1 / 11 / 11 |
| SPEI-6 | France | 8 / 18 / 16 | 3 / 6 / 6 | 2 / 6 / 6 | 1 / 1 / 6 |
| SPEI-6 | Germany | 8 / 15 / 13 | 3 / 9 / 9 | 2 / 6 / 6 | 1 / 2 / 1 |
| SPEI-6 | Sweden | 8 / 7 / 5 | 3 / 3 / 3 | 2 / 2 / 1 | 1 / 1 / 1 |

*Each TXx count is out of 90 country-month observations per period; each
SPEI-6 count is out of 30 September observations. Thresholds are early-period
percentiles, with strict inequalities and linear interpolation. Source: C3S,
Copernicus Interactive Climate Atlas v2.5, ERA5-Land, accessed 29 October
2026; `outputs/exceedance.csv`.*

Heat exceedances increase at every threshold in every country. At P95, Spain
rises from 5 to 43 observations, France from 5 to 27, Germany from 5 to 31 and
Sweden from 5 to 9. These recent exceedances come from 23, 19, 20 and 7
distinct summers, respectively. The early P95 rate is 5/90, or 5.6%, rather
than exactly 5%. The shift benchmark gives 48, 29, 27 and 9 exceedances. Thus
much of the increase can occur without a change in shape. Germany's P99 is the
clearest discrepancy: 24 observed against 14 under the benchmark. No
confidence interval is estimated for these count gaps, so they are not formal
tests of a pure shift.

Drought results depend more on the threshold. Spain has more dry observations
at all four cut-offs. France and Germany have more at P25, P10 and P5, but
France's P1 count stays at one. Sweden's counts change little. At the headline
P5, recent counts are 12, 6, 6 and 2; the shift benchmark gives 11, 6, 6 and
1. P99 for TXx and P1 for SPEI-6 each have only one early observation beyond
the line, making frequency ratios particularly unstable.

## 5.2. Tail intensity relative to the mean

We measure departure from a shift by S_p = (Q_recent,p - Q_early,p) - delta,
where Q_p is percentile p. A positive S_p means extra movement toward heat for
TXx; a negative value means extra movement toward dryness for SPEI-6. For TXx
at P95, S_p is 1.18 °C in Spain, 0.75 °C in France, 0.55 °C in Germany and
0.37 °C in Sweden. Their 95% bootstrap intervals are [-0.40, 1.72], [-0.54,
1.70], [-0.31, 1.47] and [-0.84, 1.03] °C. All include zero, as do the
corresponding intervals at the other thresholds. This is limited evidence
about tail departures, not proof of identical shapes. France and Germany
nevertheless show wider pooled distributions: their SD changes are 0.52 °C
[0.07, 0.93] and 0.59 °C [0.18, 0.98].

Intervals use 2,000 bootstrap draws, resampling years independently within
each period and keeping a summer's three months together. At each period's own
P95, only five TXx values lie above the line; at its own P5, only two SPEI-6
values lie below it. We do not detrend within periods, so changes in pooled
spread can include changes in the mean within a period (Rhines and Huybers,
2013). Resampling single years preserves dependence within summers but does
not preserve dependence across years; intervals are pointwise and do not
adjust for multiple comparisons.

## 5.3. Mean and quantile trends

For each country and index, OLS estimates y_t = alpha + beta (t - 1950)/10 +
u_t. Here t is the calendar year; y_t is the annual June-August mean TXx
anomaly (°C) or September SPEI-6 (dimensionless); alpha is the fitted level in
1950 and u_t the residual. Beta measures change per decade. Newey-West HAC
standard errors use three annual lags. Quantile regression estimates Q_tau(y |
t) = alpha_tau + beta_tau (t - 1950)/10 on pooled monthly TXx anomalies or
annual SPEI-6. We fit tau = 0.05, 0.10, 0.25, 0.50, 0.75, 0.90 and 0.95; Table
4 reports the median and relevant extreme tail.

**Table 4. Trends per decade; standard errors in parentheses.**

| Index | Country | OLS 1950-2025 | OLS 1978-2025 | QR median | QR tail |
|---|---|---|---|---|---|
| TXx | Spain | 0.440 (0.081) | 0.722 (0.085) | 0.452 (0.073) | 0.511 (0.114) |
| TXx | France | 0.550 (0.096) | 0.947 (0.117) | 0.562 (0.088) | 0.558 (0.173) |
| TXx | Germany | 0.459 (0.078) | 0.719 (0.103) | 0.466 (0.086) | 0.428 (0.158) |
| TXx | Sweden | 0.215 (0.068) | 0.296 (0.118) | 0.245 (0.114) | 0.226 (0.073) |
| SPEI-6 | Spain | -0.103 (0.048) | -0.243 (0.037) | -0.131 (0.052) | 0.017 (0.070) |
| SPEI-6 | France | -0.067 (0.053) | -0.248 (0.067) | -0.202 (0.095) | 0.024 (0.036) |
| SPEI-6 | Germany | -0.079 (0.053) | -0.223 (0.079) | -0.069 (0.072) | -0.126 (0.135) |
| SPEI-6 | Sweden | 0.027 (0.036) | -0.015 (0.064) | -0.015 (0.034) | 0.112 (0.132) |

*OLS: 76 annual values for 1950-2025 and 48 for 1978-2025, with HAC errors.
Quantile regression: 1950-2025, 228 TXx observations or 76 SPEI-6
observations; 499 whole-year bootstrap draws for standard errors. Tail means
tau = 0.95 for TXx and 0.05 for SPEI-6. Units: °C/decade for TXx, index
units/decade for SPEI-6. Source: as Table 3; `outputs/ols_trends.csv` and
`outputs/quantile_trends.csv`.*

Full-record mean TXx trends are positive in all four countries. France's 0.55
°C per decade means a fitted rise of about half a degree per decade in the
average of the three monthly maxima, not in annual mean temperature. Its
median and P95 slopes are both about 0.56 °C per decade. In every country, the
P95-minus-median slope interval includes zero; all SPEI-6 P5-minus-median
intervals also include zero. These direct contrasts provide no clear evidence
that the relevant extreme tail trends faster than the centre. They have low
precision: only 12 observations lie above each fitted TXx P95 line and five
below each SPEI-6 P5 line. Some quantile fits reach the iteration limit;
series totals range from 1 to 10 across 3,500 point and bootstrap fits, so
affected estimates remain approximate.

Re-estimating OLS from 1978 keeps positive mean TXx trends in every country
and gives negative SPEI-6 trends in Spain, France and Germany whose 95%
intervals exclude zero. Sweden's SPEI-6 interval includes zero. This addresses
the documented concern about early ERA5-Land forcing only for mean trends:
neither quantile regressions nor the early-recent comparison are re-estimated
on a wholly post-1978 sample. Different slopes across these nested samples are
not a formal test of acceleration. All regressions describe association with
time; they do not identify a causal effect.
