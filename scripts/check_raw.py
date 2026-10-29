"""Integrity check of the raw Copernicus Interactive Climate Atlas exports.

Reads every CSV in data/raw/ (read-only), parses the comment-line metadata,
computes per-file checks and descriptive range statistics, asserts that the
files are mutually consistent, then prints the table and writes it to
data/raw_check.csv.

Usage (from the repository root):
    python scripts/check_raw.py
"""

from pathlib import Path
import re

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_PATH = ROOT / "data" / "raw_check.csv"

FIRST_YEAR, LAST_YEAR = 1950, 2025
N_COMMENT_LINES = 5
INDEX_LABELS = {"txx": "TXx", "spei6": "SPEI-6"}

# Example description line:
# "Maximum of daily maximum temperature (°C) - ERA5-Land - Value - 1961-1990 - Mean of june series for Spain"
DESCRIPTION_RE = re.compile(
    r'^"(?P<variable>.+) \((?P<units>[^()]+)\) - (?P<dataset>.+?) - Value - '
    r'(?P<highlighted_period>\d{4}-\d{4}) - Mean of (?P<month>\w+) series for (?P<country>.+)"$'
)


def parse_metadata(path):
    """Return the metadata encoded in the first comment lines of a raw file."""
    with open(path, encoding="utf-8") as f:
        lines = [f.readline().rstrip("\r\n") for _ in range(N_COMMENT_LINES)]
    assert all(line.startswith("#") for line in lines), f"{path.name}: unexpected header"
    lines = [line.lstrip("#").strip() for line in lines]

    meta = {"atlas": lines[0]}
    meta["version"] = lines[1].removeprefix("Version:").strip()
    meta["generated_at"] = lines[2].removeprefix("Generated at:").strip()
    match = DESCRIPTION_RE.match(lines[4])
    assert match, f"{path.name}: cannot parse description line {lines[4]!r}"
    meta.update(match.groupdict())
    meta["month"] = meta["month"].capitalize()
    return meta


def check_file(path):
    meta = parse_metadata(path)
    df = pd.read_csv(path, skiprows=N_COMMENT_LINES)
    assert list(df.columns) == ["Year", "0"], f"{path.name}: unexpected columns {list(df.columns)}"
    years = pd.to_numeric(df["Year"], errors="coerce")
    values = pd.to_numeric(df["0"], errors="coerce")

    expected = set(range(FIRST_YEAR, LAST_YEAR + 1))
    return {
        "file": path.name,
        "index": INDEX_LABELS[path.stem.split("_")[0]],
        **{k: meta[k] for k in ["variable", "units", "dataset", "month", "country",
                                 "highlighted_period", "version", "generated_at"]},
        "n_rows": len(df),
        "first_year": int(years.min()),
        "last_year": int(years.max()),
        "missing_values": int(values.isna().sum()),
        "missing_years": len(expected - set(years.dropna().astype(int))),
        "duplicated_years": int(years.duplicated().sum()),
        "min": round(values.min(), 3),
        "mean": round(values.mean(), 3),
        "max": round(values.max(), 3),
        "sd": round(values.std(), 3),
    }


def main():
    files = sorted(RAW_DIR.glob("*.csv"))
    assert files, f"no CSV files found in {RAW_DIR}"
    table = pd.DataFrame([check_file(p) for p in files])

    n_expected = LAST_YEAR - FIRST_YEAR + 1
    assert table["version"].nunique() == 1, f"mixed Atlas versions: {table['version'].unique()}"
    assert table["dataset"].nunique() == 1, f"mixed datasets: {table['dataset'].unique()}"
    assert (table["first_year"] == FIRST_YEAR).all(), "a file does not start in 1950"
    assert (table["last_year"] == LAST_YEAR).all(), "a file does not end in 2025"
    assert (table["n_rows"] == n_expected).all(), f"a file does not have {n_expected} rows"
    assert (table["missing_years"] == 0).all(), "a file has gaps in its year sequence"
    assert (table["duplicated_years"] == 0).all(), "a file has duplicated years"
    assert (table["missing_values"] == 0).all(), "a file has missing values"

    table.to_csv(OUT_PATH, index=False)
    with pd.option_context("display.max_columns", None, "display.width", 250):
        print(table.drop(columns=["variable", "highlighted_period"]).to_string(index=False))
    print(f"\n{len(table)} files OK | version {table['version'].iloc[0]} | "
          f"dataset {table['dataset'].iloc[0]} | {FIRST_YEAR}-{LAST_YEAR} complete")
    print(f"Written to {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
