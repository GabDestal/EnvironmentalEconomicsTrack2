"""Single source of truth for paths and analysis choices.

Every script imports its periods, thresholds and settings from here.
Changing a value here and re-running `python scripts/analysis.py`
regenerates every result in outputs/.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_CHECK_PATH = ROOT / "data" / "raw_check.csv"
OUT_DIR = ROOT / "outputs"

FIRST_YEAR, LAST_YEAR = 1950, 2025

# Periods compared (group proposal in CLAUDE.md). The early period is also the
# baseline: TXx anomalies and all percentile thresholds are computed on it.
EARLY = (1961, 1990)
RECENT = (1996, 2025)

# ERA5-Land may be inconsistent before 1978 (the Atlas disables trends before
# then), so OLS trends are re-estimated from this year as a robustness check.
ROBUSTNESS_START = 1978

INDICATORS = ("TXx", "SPEI-6")
COUNTRIES = ("ESP", "FRA", "GER", "SWE")
UNITS = {"TXx": "°C", "SPEI-6": "dimensionless"}

# Heat extremes sit in the upper tail; drought extremes in the lower tail
# (negative SPEI = drier than the 1971-2005 reference climate).
TAIL_SIDE = {"TXx": "upper", "SPEI-6": "lower"}
THRESHOLD_PCTS = {"TXx": (75, 90, 95, 99), "SPEI-6": (25, 10, 5, 1)}
HEADLINE_PCT = {"TXx": 95, "SPEI-6": 5}

# tau = 0.99 is left out: with at most 228 observations only about two lie
# above it, so its slope is not identified.
QUANTILE_TAUS = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)

# Bootstrap: whole years are resampled with replacement, so the three summer
# months of a year always stay together.
N_BOOT_SHIFT = 2000
N_BOOT_QUANTREG = 499
SEED = 2026
CI_LEVEL = 0.95
