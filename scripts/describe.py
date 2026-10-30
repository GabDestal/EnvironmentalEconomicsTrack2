"""Section 3 summary statistics.

Statistics are computed on analysis_value (TXx anomaly in °C, pooled over
June-August; SPEI-6 September value). Percentiles use numpy's default linear
interpolation (Hyndman-Fan type 7).
"""

import numpy as np
import pandas as pd

from config import EARLY, RECENT, UNITS
from load_data import iter_series

SUMMARY_PCTS = (1, 5, 10, 25, 50, 75, 90, 95, 99)
PERIODS = ("early", "recent", "full")


def describe(x: np.ndarray) -> dict[str, float]:
    stats = {"n": x.size, "mean": x.mean(), "sd": x.std(ddof=1), "min": x.min()}
    stats |= {f"p{p:02d}": np.percentile(x, p) for p in SUMMARY_PCTS}
    stats["max"] = x.max()
    return stats


def summary_table(data: pd.DataFrame) -> pd.DataFrame:
    """One row per indicator, country and period (early, recent, full 1950-2025)."""
    rows = []
    for indicator, country, series in iter_series(data):
        for period in PERIODS:
            sub = series if period == "full" else series[series["period"] == period]
            rows.append({
                "indicator": indicator,
                "country": country,
                "period": period,
                "first_year": sub["year"].min(),
                "last_year": sub["year"].max(),
                "units": UNITS[indicator],
                **describe(sub["analysis_value"].to_numpy()),
            })
    return pd.DataFrame(rows)


def baseline_table(data: pd.DataFrame) -> pd.DataFrame:
    """Early-period mean TXx level (°C) of each country and month: the zero of the anomalies."""
    txx = data[data["indicator"] == "TXx"]
    table = txx.groupby(["country", "month"])["baseline_mean"].first().unstack("month")
    return table[["Jun", "Jul", "Aug"]].reset_index()


def _fmt(value: float) -> str:
    """Two decimals; adding 0.0 turns a rounded -0.0 (float noise) into 0.00."""
    return f"{round(value, 2) + 0.0:.2f}"


def _md_table(header: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def summary_markdown(summary: pd.DataFrame) -> str:
    """Table 1 of section 3: early vs recent period, two decimals."""
    cols = ["n", "mean", "sd", "min", "p05", "p25", "p50", "p75", "p95", "max"]
    header = ["Index", "Country", "Period", "N", "Mean", "SD", "Min", "P5", "P25", "Median", "P75", "P95", "Max"]
    labels = {"early": f"{EARLY[0]}-{EARLY[1]}", "recent": f"{RECENT[0]}-{RECENT[1]}"}
    rows = []
    for r in summary[summary["period"].isin(labels)].itertuples(index=False):
        values = [str(r.n)] + [_fmt(getattr(r, c)) for c in cols[1:]]
        rows.append([r.indicator, r.country, labels[r.period], *values])
    return _md_table(header, rows)


def baseline_markdown(baseline: pd.DataFrame) -> str:
    rows = [[r.country, _fmt(r.Jun), _fmt(r.Jul), _fmt(r.Aug)] for r in baseline.itertuples(index=False)]
    return _md_table(["Country", "June", "July", "August"], rows)
