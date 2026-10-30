"""Load the raw Atlas CSVs into one tidy table ready for analysis.

Output columns:
    source_file, indicator, country, month, year, value,
    period         "early", "recent" or missing (years outside both periods)
    baseline_mean  early-period mean of the same indicator, country and month
    anomaly        value - baseline_mean
    analysis_value the variable every statistic is computed on:
                   TXx -> anomaly (°C), so June, July and August can be pooled;
                   SPEI-6 -> value, already standardised by the Atlas.
"""

import re
from collections.abc import Iterator
from pathlib import Path

import pandas as pd

from config import COUNTRIES, EARLY, INDICATORS, RAW_DIR, RECENT

FILENAME_RE = re.compile(r"^(?P<prefix>txx|spei6)_(?P<country>[A-Z]{3})_(?P<month>[A-Z]{3})\.csv$")
PREFIX_TO_INDICATOR = {"txx": "TXx", "spei6": "SPEI-6"}
KEYS = ["indicator", "country", "month"]


def read_series(path: Path) -> pd.DataFrame:
    """Read one raw file (e.g. txx_ESP_JUL.csv) and label it from its file name."""
    match = FILENAME_RE.match(path.name)
    if match is None:
        raise ValueError(f"unexpected raw file name: {path.name}")
    df = pd.read_csv(path, comment="#")
    df.columns = ["year", "value"]
    return df.assign(
        source_file=path.name,
        indicator=PREFIX_TO_INDICATOR[match["prefix"]],
        country=match["country"],
        month=match["month"].capitalize(),
    )


def load_raw(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    files = sorted(raw_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"no CSV files in {raw_dir}")
    df = pd.concat([read_series(p) for p in files], ignore_index=True)
    return df[["source_file", *KEYS, "year", "value"]]


def assign_period(years: pd.Series, early: tuple[int, int], recent: tuple[int, int]) -> pd.Series:
    period = pd.Series(pd.NA, index=years.index, dtype="string")
    period[years.between(*early)] = "early"
    period[years.between(*recent)] = "recent"
    return period


def add_anomaly(df: pd.DataFrame, baseline: tuple[int, int]) -> pd.DataFrame:
    """Add each series' mean over the baseline years and the deviation from it."""
    baseline_mean = (
        df[df["year"].between(*baseline)]
        .groupby(KEYS)["value"].mean()
        .rename("baseline_mean")
    )
    out = df.join(baseline_mean, on=KEYS)
    return out.assign(anomaly=out["value"] - out["baseline_mean"])


def build_analysis_data(raw: pd.DataFrame, early: tuple[int, int], recent: tuple[int, int]) -> pd.DataFrame:
    df = add_anomaly(raw, baseline=early)
    df["period"] = assign_period(df["year"], early, recent)
    df["analysis_value"] = df["anomaly"].where(df["indicator"] == "TXx", df["value"])
    return df.sort_values([*KEYS, "year"]).reset_index(drop=True)


def load_analysis_data(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Entry point for other scripts (figures, econometrics): the tidy analysis table."""
    return build_analysis_data(load_raw(raw_dir), EARLY, RECENT)


def iter_series(data: pd.DataFrame) -> Iterator[tuple[str, str, pd.DataFrame]]:
    """Yield (indicator, country, rows) in the fixed order of config.py, skipping absent ones."""
    for indicator in INDICATORS:
        for country in COUNTRIES:
            rows = data[(data["indicator"] == indicator) & (data["country"] == country)]
            if not rows.empty:
                yield indicator, country, rows
