import numpy as np
import pytest

from bootstrap import percentile_ci, year_bootstrap


def test_year_bootstrap_keeps_all_rows_of_a_year_together():
    years = np.repeat([1, 2, 3, 4], 3)
    for rows in year_bootstrap(years, n_boot=50, rng=np.random.default_rng(0)):
        assert rows.size == years.size
        drawn_years, counts = np.unique(years[rows], return_counts=True)
        assert (counts % 3 == 0).all()
        assert set(drawn_years) <= {1, 2, 3, 4}


def test_year_bootstrap_is_reproducible_with_the_same_seed():
    years = np.arange(30)
    first = list(year_bootstrap(years, 5, np.random.default_rng(42)))
    second = list(year_bootstrap(years, 5, np.random.default_rng(42)))
    assert all((a == b).all() for a, b in zip(first, second))


def test_percentile_ci_cuts_equal_tails():
    lo, hi = percentile_ci(np.arange(1001, dtype=float), level=0.95)
    assert lo == pytest.approx(25.0) and hi == pytest.approx(975.0)
