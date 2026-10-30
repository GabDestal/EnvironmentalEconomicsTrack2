from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from config import COUNTRIES, EARLY, FIRST_YEAR, LAST_YEAR, RECENT
from load_data import KEYS, add_anomaly, assign_period, build_analysis_data, load_analysis_data, read_series

HEADER = (
    "# Copernicus Interactive Climate Atlas - Regional information\n"
    "# Version: v2.5\n"
    "# Generated at: 2026-10-29T16:13:30.398Z\n"
    "# Columns: year, model, value\n"
    '# "Maximum of daily maximum temperature (°C) - ERA5-Land - Value - 1961-1990 - Mean of july series for Spain"\n'
    "Year,0\n"
)


def write_raw(path: Path, rows: list[tuple[int, float]]) -> Path:
    path.write_text(HEADER + "".join(f"{y},{v}\n" for y, v in rows), encoding="utf-8")
    return path


def test_read_series_labels_rows_from_file_name(tmp_path):
    df = read_series(write_raw(tmp_path / "txx_ESP_JUL.csv", [(1950, 34.5), (1951, 35.6)]))
    assert df["year"].tolist() == [1950, 1951]
    assert df["value"].tolist() == [34.5, 35.6]
    assert df[["indicator", "country", "month"]].drop_duplicates().values.tolist() == [["TXx", "ESP", "Jul"]]


def test_read_series_rejects_unknown_file_name(tmp_path):
    with pytest.raises(ValueError):
        read_series(write_raw(tmp_path / "tx_ESP_JUL.csv", [(1950, 1.0)]))


def test_assign_period_marks_only_years_inside_periods():
    years = pd.Series([1960, 1961, 1990, 1991, 1995, 1996, 2025])
    period = assign_period(years, (1961, 1990), (1996, 2025)).fillna("none")
    assert period.tolist() == ["none", "early", "early", "none", "none", "recent", "recent"]


def test_add_anomaly_uses_baseline_mean_of_each_series():
    df = pd.DataFrame({
        "indicator": "TXx",
        "country": "ESP",
        "month": ["Jun"] * 3 + ["Jul"] * 3,
        "year": [2000, 2001, 2002] * 2,
        "value": [10.0, 12.0, 20.0, 30.0, 34.0, 40.0],
    })
    out = add_anomaly(df, baseline=(2000, 2001))
    assert out["baseline_mean"].tolist() == [11.0] * 3 + [32.0] * 3
    assert out["anomaly"].tolist() == [-1.0, 1.0, 9.0, -2.0, 2.0, 8.0]


def test_analysis_value_is_anomaly_for_txx_and_raw_value_for_spei():
    df = pd.DataFrame({
        "source_file": "f.csv",
        "indicator": ["TXx", "TXx", "SPEI-6", "SPEI-6"],
        "country": "ESP",
        "month": ["Jul", "Jul", "Sep", "Sep"],
        "year": [2000, 2001, 2000, 2001],
        "value": [30.0, 32.0, -0.5, 0.5],
    })
    out = build_analysis_data(df, early=(2000, 2000), recent=(2001, 2001))
    assert out.loc[out["indicator"] == "TXx", "analysis_value"].tolist() == [0.0, 2.0]
    assert out.loc[out["indicator"] == "SPEI-6", "analysis_value"].tolist() == [-0.5, 0.5]


def test_real_data_is_complete_and_balanced_by_period():
    data = load_analysis_data()
    assert len(data) == 16 * (LAST_YEAR - FIRST_YEAR + 1)
    assert set(data["country"]) == set(COUNTRIES)

    years_in = {"early": EARLY[1] - EARLY[0] + 1, "recent": RECENT[1] - RECENT[0] + 1}
    sizes = data.dropna(subset=["period"]).groupby(["indicator", "country", "period"]).size()
    for (indicator, _, period), n in sizes.items():
        months = 3 if indicator == "TXx" else 1
        assert n == years_in[period] * months

    early = data[data["period"] == "early"]
    assert np.allclose(early.groupby(KEYS)["anomaly"].mean(), 0.0, atol=1e-10)
