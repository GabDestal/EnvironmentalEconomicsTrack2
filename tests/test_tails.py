import numpy as np
import pytest

from tails import beyond, exceedance_table, shift_shape_table


def run_shift_shape(data):
    return shift_shape_table(data, n_boot=200, seed=0, ci_level=0.95).set_index("tail_pct")


def test_beyond_is_strict_on_both_sides():
    x = np.array([1.0, 2.0, 3.0])
    assert beyond(x, 2.0, "upper").tolist() == [False, False, True]
    assert beyond(x, 2.0, "lower").tolist() == [True, False, False]
    with pytest.raises(ValueError):
        beyond(x, 2.0, "both")


def test_pure_shift_gives_zero_shape(make_data):
    early = np.linspace(-2, 2, 90)
    table = run_shift_shape(make_data(early, early + 1.5, per_year=3))
    assert np.allclose(table["d_mean"], 1.5)
    assert np.allclose(table["d_q"], 1.5)
    assert np.allclose(table["shape"], 0.0, atol=1e-12)
    assert (table["shape_lo"] <= 1e-12).all() and (table["shape_hi"] >= -1e-12).all()


def test_stretched_upper_tail_gives_positive_shape_for_txx(make_data):
    early = np.linspace(-2, 2, 90)
    table = run_shift_shape(make_data(early, 2 * early, per_year=3))
    assert table.loc[95, "d_mean"] == pytest.approx(0.0, abs=1e-12)
    assert table.loc[95, "shape"] > 0
    assert table.loc[95, "shape_extreme"] == table.loc[95, "shape"]
    assert table.loc[95, "headline"]
    # Values rise with the row, so the top 5 of 90 rows sit in the last 2 of 30 years.
    assert table.loc[95, "n_beyond_early"] == 5
    assert table.loc[95, "years_beyond_early"] == 2


def test_spei_uses_lower_tail(make_data):
    early = np.linspace(-2, 2, 30)
    table = run_shift_shape(make_data(early, 2 * early, indicator="SPEI-6"))
    assert list(table.index) == [25, 10, 5, 1]
    assert (table["side"] == "lower").all()
    assert table.loc[5, "shape"] < 0
    assert table.loc[5, "shape_extreme"] == -table.loc[5, "shape"] > 0
    assert table.loc[5, "shape_extreme_lo"] == -table.loc[5, "shape_hi"]
    assert table.loc[5, "shape_extreme_hi"] == -table.loc[5, "shape_lo"]
    assert table.loc[5, "headline"]


def test_exceedance_counts_upper_tail(make_data):
    early = np.arange(1, 101)
    table = exceedance_table(make_data(early, early + 10)).set_index("threshold_pct")
    assert table.loc[90, "threshold_value"] == pytest.approx(90.1)
    assert table.loc[90, ["k_early", "k_recent", "k_shift_only"]].tolist() == [10, 20, 20]
    assert table.loc[90, ["years_early", "years_recent"]].tolist() == [10, 20]
    assert table.loc[99, ["k_early", "k_recent"]].tolist() == [1, 11]
    assert table.loc[90, "rate_ratio"] == pytest.approx(2.0)
    assert np.allclose(table["excess_over_shift"], 0.0)


def test_exceedance_counts_lower_tail_for_spei(make_data):
    early = np.arange(1, 101)
    table = exceedance_table(make_data(early, early - 10, indicator="SPEI-6")).set_index("threshold_pct")
    assert table.loc[10, "threshold_value"] == pytest.approx(10.9)
    assert table.loc[10, ["k_early", "k_recent"]].tolist() == [10, 20]
    assert table.loc[1, ["k_early", "k_recent"]].tolist() == [1, 11]


def test_rate_ratio_is_missing_when_early_period_has_no_exceedance(make_data):
    table = exceedance_table(make_data(np.ones(10), 2 * np.ones(10)))
    assert table["k_early"].eq(0).all()
    assert table["rate_ratio"].isna().all()
