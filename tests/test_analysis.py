import numpy as np
import pandas as pd

from analysis import round_floats
from config import OUT_DIR
from load_data import load_raw


def test_round_floats_rounds_floats_only_and_removes_negative_zero():
    df = pd.DataFrame({"x": [1.23456, -1e-16, np.nan], "n": [1, 2, 3], "label": ["a", "b", "c"]})
    out = round_floats(df, 4)
    assert out["x"].iloc[0] == 1.2346
    assert str(out["x"].iloc[1]) == "0.0"
    assert np.isnan(out["x"].iloc[2])
    assert out["n"].tolist() == [1, 2, 3] and out["label"].tolist() == ["a", "b", "c"]


def test_tidy_output_keeps_raw_values_exactly():
    written = pd.read_csv(OUT_DIR / "analysis_data.csv")
    merged = written.merge(load_raw(), on=["source_file", "year"], suffixes=("_written", "_raw"))
    assert len(merged) == len(written) == 16 * 76
    assert (merged["value_written"] == merged["value_raw"]).all()
