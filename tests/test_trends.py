import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from trends import decades_since_start, newey_west_lags, ols_trend, ols_trend_table, quantile_trend_table

YEARS = np.arange(1950, 2026)


def summer_data(values_for_month) -> pd.DataFrame:
    """Synthetic pooled TXx table for one country: one row per year and summer month."""
    frames = [
        pd.DataFrame({"indicator": "TXx", "country": "ESP", "month": m, "year": YEARS,
                      "analysis_value": values_for_month(m)})
        for m in ("Jun", "Jul", "Aug")
    ]
    return pd.concat(frames, ignore_index=True)


def test_newey_west_rule_of_thumb():
    assert newey_west_lags(76) == 3
    assert newey_west_lags(100) == 4


def test_ols_trend_recovers_slope_per_decade():
    noise = 0.5 * (-1.0) ** YEARS
    result = ols_trend(YEARS, 2 + 0.3 * decades_since_start(YEARS) + noise, ci_level=0.95)
    assert result["slope_per_decade"] == pytest.approx(0.3, abs=0.01)
    assert result["n"] == 76 and result["hac_lags"] == 3
    assert result["ci_lo"] < result["slope_per_decade"] < result["ci_hi"]


def test_summer_mean_slope_equals_pooled_ols_slope():
    rng = np.random.default_rng(1)
    data = summer_data(lambda m: 0.25 * decades_since_start(YEARS) + rng.normal(size=YEARS.size))
    table = ols_trend_table(data, ci_level=0.95)
    assert table["series"].unique().tolist() == ["Jun", "Jul", "Aug", "Jun-Aug mean"]
    assert table["sample"].unique().tolist() == ["1950-2025", "1978-2025"]

    pooled = sm.OLS(data["analysis_value"], sm.add_constant(decades_since_start(data["year"]))).fit()
    summer = table[(table["series"] == "Jun-Aug mean") & (table["sample"] == "1950-2025")]
    assert summer["slope_per_decade"].item() == pytest.approx(pooled.params.iloc[1])
    assert table.loc[table["sample"] == "1978-2025", "n"].unique().tolist() == [48]


def test_quantile_slopes_fan_out_when_spread_grows():
    rng = np.random.default_rng(2)
    data = summer_data(lambda m: (1 + decades_since_start(YEARS)) * rng.uniform(-1, 1, YEARS.size))
    table = quantile_trend_table(data, (0.05, 0.5, 0.95), n_boot=40, seed=0, ci_level=0.95).set_index("tau")

    assert table.loc[0.95, "slope_per_decade"] == pytest.approx(0.9, abs=0.3)
    assert table.loc[0.05, "slope_per_decade"] == pytest.approx(-0.9, abs=0.3)
    assert table.loc[0.95, "minus_median_lo"] > 0
    assert table.loc[0.5, "minus_median"] == 0
    assert table.loc[0.95, "n_beyond_line"] == pytest.approx(0.05 * 228, abs=4)
    assert (table["ci_lo"] <= table["ci_hi"]).all()


def test_quantile_trend_table_requires_the_median():
    with pytest.raises(ValueError):
        quantile_trend_table(summer_data(lambda m: np.zeros(YEARS.size)), (0.1, 0.9), 10, 0, 0.95)
