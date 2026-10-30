"""Tail analysis: has the distribution shifted, or has its tail changed shape?

Two complementary views, both comparing the early with the recent period:

- Intensity (shift_shape_table): change in a tail percentile versus change in
  the mean. If the whole distribution moved, the two are equal; the
  difference d_q - d_mean ("shape") measures how much the tail moved beyond
  the shift. Bootstrap confidence intervals resample whole years.
- Frequency (exceedance_table): share of observations beyond a threshold set
  on the early period, in each period, and the share the recent period would
  have if the early distribution had only shifted by d_mean.

Heat extremes are the upper tail of TXx; drought extremes the lower tail of
SPEI-6, so "beyond" means above for TXx and below for SPEI-6. The raw shape
is therefore positive for a heavier TXx tail but negative for a heavier
SPEI-6 tail; shape_extreme flips the SPEI-6 sign so that, for both indices,
shape_extreme > 0 means the tail moved further toward the extreme than the
mean did.

Pooled TXx months of the same summer are correlated, so next to each count
of tail observations we report the number of distinct years behind it.
"""

import numpy as np
import pandas as pd

from bootstrap import percentile_ci, year_bootstrap
from config import HEADLINE_PCT, TAIL_SIDE, THRESHOLD_PCTS
from load_data import iter_series


def beyond(x: np.ndarray, threshold: float, side: str) -> np.ndarray:
    if side == "upper":
        return x > threshold
    if side == "lower":
        return x < threshold
    raise ValueError(f"side must be 'upper' or 'lower', got {side!r}")


def _period_arrays(series: pd.DataFrame, period: str) -> tuple[np.ndarray, np.ndarray]:
    sub = series[series["period"] == period]
    return sub["analysis_value"].to_numpy(), sub["year"].to_numpy()


def shift_shape_table(data: pd.DataFrame, n_boot: int, seed: int, ci_level: float) -> pd.DataFrame:
    rows = []
    for indicator, country, series in iter_series(data):
        side, pcts = TAIL_SIDE[indicator], np.array(THRESHOLD_PCTS[indicator])
        e_x, e_years = _period_arrays(series, "early")
        r_x, r_years = _period_arrays(series, "recent")

        q_early, q_recent = np.percentile(e_x, pcts), np.percentile(r_x, pcts)
        d_mean, d_sd = r_x.mean() - e_x.mean(), r_x.std(ddof=1) - e_x.std(ddof=1)
        d_q = q_recent - q_early

        rng = np.random.default_rng(seed)
        boot_mean, boot_sd = np.empty(n_boot), np.empty(n_boot)
        boot_q = np.empty((n_boot, pcts.size))
        draws = zip(year_bootstrap(e_years, n_boot, rng), year_bootstrap(r_years, n_boot, rng))
        for b, (ei, ri) in enumerate(draws):
            e_b, r_b = e_x[ei], r_x[ri]
            boot_mean[b] = r_b.mean() - e_b.mean()
            boot_sd[b] = r_b.std(ddof=1) - e_b.std(ddof=1)
            boot_q[b] = np.percentile(r_b, pcts) - np.percentile(e_b, pcts)
        mean_lo, mean_hi = percentile_ci(boot_mean, ci_level)
        sd_lo, sd_hi = percentile_ci(boot_sd, ci_level)
        q_lo, q_hi = percentile_ci(boot_q, ci_level)
        shape_lo, shape_hi = percentile_ci(boot_q - boot_mean[:, None], ci_level)
        sign = 1 if side == "upper" else -1

        for j, pct in enumerate(pcts):
            tail_e, tail_r = beyond(e_x, q_early[j], side), beyond(r_x, q_recent[j], side)
            extreme_bounds = sorted([sign * shape_lo[j], sign * shape_hi[j]])
            rows.append({
                "indicator": indicator, "country": country, "side": side,
                "tail_pct": int(pct), "headline": bool(pct == HEADLINE_PCT[indicator]),
                "n_early": e_x.size, "n_recent": r_x.size,
                "mean_early": e_x.mean(), "mean_recent": r_x.mean(),
                "d_mean": d_mean, "d_mean_lo": mean_lo, "d_mean_hi": mean_hi,
                "d_sd": d_sd, "d_sd_lo": sd_lo, "d_sd_hi": sd_hi,
                "q_early": q_early[j], "q_recent": q_recent[j],
                "d_q": d_q[j], "d_q_lo": q_lo[j], "d_q_hi": q_hi[j],
                "shape": d_q[j] - d_mean, "shape_lo": shape_lo[j], "shape_hi": shape_hi[j],
                "shape_extreme": sign * (d_q[j] - d_mean),
                "shape_extreme_lo": extreme_bounds[0], "shape_extreme_hi": extreme_bounds[1],
                "n_beyond_early": int(tail_e.sum()), "years_beyond_early": np.unique(e_years[tail_e]).size,
                "n_beyond_recent": int(tail_r.sum()), "years_beyond_recent": np.unique(r_years[tail_r]).size,
            })
    return pd.DataFrame(rows)


def exceedance_table(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for indicator, country, series in iter_series(data):
        side = TAIL_SIDE[indicator]
        e_x, e_years = _period_arrays(series, "early")
        r_x, r_years = _period_arrays(series, "recent")
        shifted = e_x + (r_x.mean() - e_x.mean())

        for pct in THRESHOLD_PCTS[indicator]:
            threshold = np.percentile(e_x, pct)
            hit_early, hit_recent = beyond(e_x, threshold, side), beyond(r_x, threshold, side)
            k_early, k_recent = int(hit_early.sum()), int(hit_recent.sum())
            k_shift = int(beyond(shifted, threshold, side).sum())
            rate_early, rate_recent = k_early / e_x.size, k_recent / r_x.size
            rate_shift = k_shift / e_x.size
            rows.append({
                "indicator": indicator, "country": country, "side": side,
                "threshold_pct": pct, "threshold_value": threshold,
                "n_early": e_x.size, "k_early": k_early, "rate_early": rate_early,
                "years_early": np.unique(e_years[hit_early]).size,
                "n_recent": r_x.size, "k_recent": k_recent, "rate_recent": rate_recent,
                "years_recent": np.unique(r_years[hit_recent]).size,
                "rate_ratio": rate_recent / rate_early if k_early else np.nan,
                "k_shift_only": k_shift, "rate_shift_only": rate_shift,
                "excess_over_shift": rate_recent - rate_shift,
            })
    return pd.DataFrame(rows)
