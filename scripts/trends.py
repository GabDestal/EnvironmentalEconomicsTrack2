"""Trend estimation: OLS with HAC standard errors and quantile regression on time.

Model:  y_t = a + b * (year_t - 1950) / 10 + u_t
so b is the change per decade in the units of the index (°C for TXx
anomalies, SPEI-6 units for SPEI-6).

OLS uses one observation per year. For TXx the yearly series is the mean of
the June, July and August anomalies: its slope equals the slope of OLS on
the pooled months, but it is a proper time series, which Newey-West (HAC)
errors require. Each month is also estimated on its own.

Quantile regression uses the pooled observations (three per year for TXx).
Standard errors and intervals come from the year-block bootstrap, because
statsmodels' analytical errors assume independent rows. Each draw re-fits
every tau on the same resampled years, so the difference between a tail
slope and the median slope gets its own interval. series_nonconverged_boot_fits
counts, over all taus and draws of a series, the fits that hit the iteration
limit (their slope is an approximation).
"""

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
from statsmodels.tools.sm_exceptions import IterationLimitWarning

from bootstrap import percentile_ci, year_bootstrap
from config import FIRST_YEAR, LAST_YEAR, ROBUSTNESS_START
from load_data import iter_series

MONTH_ORDER = ("Jun", "Jul", "Aug", "Sep")
QR_MAX_ITER = 5000


def decades_since_start(years: np.ndarray) -> np.ndarray:
    return (np.asarray(years, dtype=float) - FIRST_YEAR) / 10


def newey_west_lags(n: int) -> int:
    """Newey-West (1994) rule of thumb: floor(4 * (n / 100) ** (2 / 9))."""
    return int(np.floor(4 * (n / 100) ** (2 / 9)))


def ols_trend(years: np.ndarray, y: np.ndarray, ci_level: float) -> dict[str, float]:
    lags = newey_west_lags(y.size)
    X = sm.add_constant(decades_since_start(years))
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": lags}, use_t=True)
    ci_lo, ci_hi = fit.conf_int(alpha=1 - ci_level)[1]
    return {
        "n": y.size, "hac_lags": lags,
        "slope_per_decade": fit.params[1], "se_hac": fit.bse[1],
        "t_stat": fit.tvalues[1], "p_value": fit.pvalues[1],
        "ci_lo": ci_lo, "ci_hi": ci_hi,
    }


def yearly_series(indicator: str, rows: pd.DataFrame) -> dict[str, pd.Series]:
    """One value per year: each month separately, plus the June-August mean for TXx."""
    out = {
        month: rows[rows["month"] == month].set_index("year")["analysis_value"].sort_index()
        for month in MONTH_ORDER if (rows["month"] == month).any()
    }
    if indicator == "TXx":
        out["Jun-Aug mean"] = rows.groupby("year")["analysis_value"].mean()
    return out


def ols_trend_table(data: pd.DataFrame, ci_level: float) -> pd.DataFrame:
    samples = [(FIRST_YEAR, LAST_YEAR), (ROBUSTNESS_START, LAST_YEAR)]
    rows = []
    for indicator, country, series in iter_series(data):
        for name, y in yearly_series(indicator, series).items():
            for start, end in samples:
                y_s = y.loc[start:end]
                rows.append({
                    "indicator": indicator, "country": country, "series": name,
                    "sample": f"{start}-{end}",
                    **ols_trend(y_s.index.to_numpy(), y_s.to_numpy(), ci_level),
                })
    return pd.DataFrame(rows)


def _qr_fit(X: np.ndarray, y: np.ndarray, taus: np.ndarray) -> list:
    model = QuantReg(y, X)
    return [model.fit(q=tau, max_iter=QR_MAX_ITER) for tau in taus]


def quantile_trend_table(
    data: pd.DataFrame, taus: tuple[float, ...], n_boot: int, seed: int, ci_level: float
) -> pd.DataFrame:
    taus = np.asarray(taus, dtype=float)
    if not np.isclose(taus, 0.5).any():
        raise ValueError("taus must include the median (0.5)")
    median = int(np.flatnonzero(np.isclose(taus, 0.5))[0])

    rows = []
    for indicator, country, series in iter_series(data):
        years = series["year"].to_numpy()
        y = series["analysis_value"].to_numpy()
        X = sm.add_constant(decades_since_start(years))

        fits = _qr_fit(X, y, taus)
        slopes = np.array([f.params[1] for f in fits])
        n_beyond = [int((f.resid > 0).sum() if tau >= 0.5 else (f.resid < 0).sum()) for f, tau in zip(fits, taus)]

        rng = np.random.default_rng(seed)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", IterationLimitWarning)
            boot = np.array([
                [f.params[1] for f in _qr_fit(X[idx], y[idx], taus)]
                for idx in year_bootstrap(years, n_boot, rng)
            ])
        n_warnings = sum(issubclass(w.category, IterationLimitWarning) for w in caught)

        se = boot.std(axis=0, ddof=1)
        ci_lo, ci_hi = percentile_ci(boot, ci_level)
        diff_lo, diff_hi = percentile_ci(boot - boot[:, [median]], ci_level)
        for j, tau in enumerate(taus):
            rows.append({
                "indicator": indicator, "country": country, "tau": tau,
                "sample": f"{years.min()}-{years.max()}", "n": y.size, "n_beyond_line": n_beyond[j],
                "slope_per_decade": slopes[j], "boot_se": se[j], "ci_lo": ci_lo[j], "ci_hi": ci_hi[j],
                "minus_median": slopes[j] - slopes[median],
                "minus_median_lo": diff_lo[j], "minus_median_hi": diff_hi[j],
                "n_boot": n_boot, "series_nonconverged_boot_fits": n_warnings,
            })
    return pd.DataFrame(rows)
