import figures


def test_every_figure_is_written(tmp_path, monkeypatch):
    monkeypatch.setattr(figures, "FIG_DIR", tmp_path)
    figures.main()
    names = sorted(p.name for p in tmp_path.glob("*.png"))
    assert names == [
        "fig1_txx_timeseries.png",
        "fig2_txx_distributions.png",
        "fig3_txx_shift_vs_shape.png",
        "fig4_txx_thresholds.png",
        "fig5_spei_drought.png",
    ]
