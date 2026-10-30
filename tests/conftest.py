import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def make_data():
    """Build a minimal analysis table with an early and a recent period.

    per_year > 1 gives several rows per year, like pooled June-August TXx.
    """

    def _make(early, recent, indicator="TXx", country="ESP", per_year=1):
        def block(values, period, start_year):
            values = np.asarray(values, dtype=float)
            years = start_year + np.repeat(np.arange(values.size // per_year), per_year)
            return pd.DataFrame({
                "indicator": indicator,
                "country": country,
                "period": period,
                "year": years,
                "analysis_value": values,
            })

        return pd.concat([block(early, "early", 1000), block(recent, "recent", 2000)], ignore_index=True)

    return _make
