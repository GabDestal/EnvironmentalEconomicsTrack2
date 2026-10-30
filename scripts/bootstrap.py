"""Year-block bootstrap used for every confidence interval in the pipeline.

Pooled TXx has three observations per year (June, July, August) that are not
independent: a hot summer tends to raise all three. Whole years are therefore
resampled with replacement, keeping a year's months together. For SPEI-6 a
year is one observation and this is the ordinary bootstrap.
"""

from collections.abc import Iterator

import numpy as np


def year_bootstrap(years: np.ndarray, n_boot: int, rng: np.random.Generator) -> Iterator[np.ndarray]:
    """Yield n_boot arrays of row positions, each built from whole resampled years."""
    unique_years = np.unique(years)
    rows_of_year = [np.flatnonzero(years == y) for y in unique_years]
    for _ in range(n_boot):
        drawn = rng.integers(0, unique_years.size, size=unique_years.size)
        yield np.concatenate([rows_of_year[i] for i in drawn])


def percentile_ci(draws: np.ndarray, level: float) -> tuple[np.ndarray, np.ndarray]:
    """Percentile confidence interval of bootstrap draws (along the first axis)."""
    alpha = (1 - level) / 2
    return np.quantile(draws, alpha, axis=0), np.quantile(draws, 1 - alpha, axis=0)
