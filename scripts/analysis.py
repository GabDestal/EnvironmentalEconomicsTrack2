"""Reproduce every result of the paper from the raw files in data/raw/.

Usage (from the repository root):
    python scripts/analysis.py

Writes to outputs/ (generated files: never edit them by hand):
    analysis_data.csv    tidy data behind every result, one row per series and year
    summary_stats.csv    section 3: N, mean, SD, percentiles by indicator, country, period
    table_summary.md     the same, early vs recent, formatted for the paper (Table 1)
    txx_baseline.csv/md  early-period mean TXx level (°C) per country and month
    shift_shape.csv      change in tail percentiles vs change in the mean, bootstrap CIs
    exceedance.csv       exceedances of early-period thresholds, observed and under a pure shift
    ols_trends.csv       OLS trend per decade with HAC standard errors
    quantile_trends.csv  quantile-regression trend per decade with bootstrap standard errors

All periods, thresholds and settings come from scripts/config.py.
"""

import pandas as pd

from config import CI_LEVEL, EARLY, N_BOOT_QUANTREG, N_BOOT_SHIFT, OUT_DIR, QUANTILE_TAUS, RECENT, ROOT, SEED
from describe import baseline_markdown, baseline_table, summary_markdown, summary_table
from load_data import load_analysis_data
from tails import exceedance_table, shift_shape_table
from trends import ols_trend_table, quantile_trend_table

# Float differences between machines stay far below these precisions, so the
# written files should match. The tidy data keeps enough digits to hold raw values.
DERIVED_DECIMALS = 4
TIDY_DECIMALS = 10


def round_floats(df: pd.DataFrame, decimals: int) -> pd.DataFrame:
    """Round float columns; adding 0.0 turns -0.0 (noise around zero) into 0.0."""
    floats = df.select_dtypes("float").columns
    return df.assign(**{col: df[col].round(decimals) + 0.0 for col in floats})


def write_csv(df: pd.DataFrame, name: str, decimals: int = DERIVED_DECIMALS) -> None:
    path = OUT_DIR / f"{name}.csv"
    round_floats(df, decimals).to_csv(path, index=False)
    print(f"  {path.relative_to(ROOT)} ({len(df)} rows)")


def write_text(text: str, name: str) -> None:
    path = OUT_DIR / name
    path.write_text(text, encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}")


def print_headline(shift_shape: pd.DataFrame) -> None:
    cols = ["indicator", "country", "tail_pct", "n_early", "n_beyond_early",
            "d_mean", "d_q", "shape", "shape_lo", "shape_hi"]
    headline = shift_shape.loc[shift_shape["headline"], cols]
    print("\nShift vs shape (headline percentile; shape = d_q - d_mean, 95% bootstrap CI):")
    print(headline.to_string(index=False, float_format=lambda v: f"{v:.2f}"))


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Early period {EARLY[0]}-{EARLY[1]}, recent period {RECENT[0]}-{RECENT[1]}")

    data = load_analysis_data()
    summary = summary_table(data)
    baseline = baseline_table(data)
    shift_shape = shift_shape_table(data, N_BOOT_SHIFT, SEED, CI_LEVEL)
    exceedance = exceedance_table(data)
    ols = ols_trend_table(data, CI_LEVEL)
    print(f"Quantile regression bootstrap ({N_BOOT_QUANTREG} draws per series), a few minutes...")
    quantile = quantile_trend_table(data, QUANTILE_TAUS, N_BOOT_QUANTREG, SEED, CI_LEVEL)

    print("Written:")
    write_csv(data, "analysis_data", decimals=TIDY_DECIMALS)
    write_csv(summary, "summary_stats")
    write_csv(baseline, "txx_baseline")
    write_csv(shift_shape, "shift_shape")
    write_csv(exceedance, "exceedance")
    write_csv(ols, "ols_trends")
    write_csv(quantile, "quantile_trends")
    write_text(summary_markdown(summary), "table_summary.md")
    write_text(baseline_markdown(baseline), "txx_baseline.md")

    print_headline(shift_shape)


if __name__ == "__main__":
    main()
