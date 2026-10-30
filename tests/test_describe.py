import numpy as np
import pandas as pd
import pytest

from config import EARLY, RAW_CHECK_PATH, RAW_DIR
from describe import baseline_table, describe, summary_markdown, summary_table
from load_data import load_analysis_data, load_raw


@pytest.fixture(scope="module")
def data():
    return load_analysis_data()


def test_describe_on_known_values():
    stats = describe(np.arange(1, 102, dtype=float))
    assert stats["n"] == 101
    assert stats["mean"] == 51 and stats["p50"] == 51
    assert stats["min"] == 1 and stats["max"] == 101
    assert stats["p05"] == pytest.approx(6.0) and stats["p95"] == pytest.approx(96.0)
    assert stats["sd"] == pytest.approx(np.arange(1, 102).std(ddof=1))


def test_loaded_values_match_part_a_raw_check():
    raw = load_raw()
    stats = raw.groupby("source_file")["value"].agg(["min", "mean", "max", "std"]).round(3)
    check = pd.read_csv(RAW_CHECK_PATH).set_index("file")
    assert set(stats.index) == set(check.index)
    for col, check_col in [("min", "min"), ("mean", "mean"), ("max", "max"), ("std", "sd")]:
        assert np.allclose(stats[col], check.loc[stats.index, check_col], atol=1e-9)


def test_summary_table_counts_and_baseline_zero(data):
    summary = summary_table(data).set_index(["indicator", "country", "period"])
    assert len(summary) == 2 * 4 * 3
    assert (summary.xs("TXx")["n"].unstack()[["early", "recent", "full"]].values == [90, 90, 228]).all()
    assert (summary.xs("SPEI-6")["n"].unstack()[["early", "recent", "full"]].values == [30, 30, 76]).all()
    assert np.allclose(summary.xs(("TXx", "ESP", "early"))["mean"], 0.0, atol=1e-10)
    assert summary.xs(("SPEI-6", "SWE", "full"))[["first_year", "last_year"]].tolist() == [1950, 2025]


def test_baseline_table_is_early_mean_of_raw_file(data):
    raw = pd.read_csv(RAW_DIR / "txx_ESP_JUL.csv", comment="#")
    raw.columns = ["year", "value"]
    expected = raw.loc[raw["year"].between(*EARLY), "value"].mean()
    baseline = baseline_table(data).set_index("country")
    assert baseline.loc["ESP", "Jul"] == pytest.approx(expected)
    assert list(baseline.index) == ["ESP", "FRA", "GER", "SWE"]


def test_summary_markdown_has_one_row_per_indicator_country_period(data):
    md = summary_markdown(summary_table(data)).strip().splitlines()
    assert len(md) == 2 + 16
    assert f"{EARLY[0]}-{EARLY[1]}" in md[2]
