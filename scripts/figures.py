"""Figures for section 4 of the paper.

Run after analysis.py, from the repository root:
    python scripts/figures.py

Every figure is drawn from load_analysis_data() or the CSVs in outputs/, with
periods and thresholds from config.py, so nothing here is typed by hand.
PNGs are written to outputs/figures/.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import COUNTRIES, EARLY, OUT_DIR, RECENT, ROBUSTNESS_START
from load_data import load_analysis_data

FIG_DIR = OUT_DIR / "figures"
NAMES = {"ESP": "Spain", "FRA": "France", "GER": "Germany", "SWE": "Sweden"}
# Two colours checked for colour-blind separation; early also drawn hollow/dashed.
C_EARLY, C_RECENT, C_INK, C_MUTED = "#3b6ea8", "#c2410c", "#222222", "#6b6b6b"
SOURCE = "Source: Copernicus Interactive Climate Atlas v2.5, ERA5-Land, accessed 29 Oct 2026."
EARLY_LBL = f"Early {EARLY[0]}–{EARLY[1]}"
RECENT_LBL = f"Recent {RECENT[0]}–{RECENT[1]}"

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": C_MUTED, "axes.labelcolor": C_INK,
    "xtick.color": C_MUTED, "ytick.color": C_MUTED,
    "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.6,
    "legend.frameon": False, "savefig.dpi": 200, "savefig.bbox": "tight",
})


def grid(title: str, note: str):
    fig, axes = plt.subplots(2, 2, figsize=(8, 5.6), sharex=True, sharey=True)
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.text(0.01, -0.01, f"{note} {SOURCE}", ha="left", va="top", fontsize=7.5,
             color=C_MUTED, wrap=True)
    return fig, dict(zip(COUNTRIES, axes.flat))


def fig_legend(fig, ax) -> None:
    h, l = ax.get_legend_handles_labels()
    fig.legend(h, l, loc="upper left", ncol=len(l), fontsize=8, bbox_to_anchor=(0.005, 0.955))


def save(fig, name: str) -> None:
    fig.tight_layout(rect=(0, 0.02, 1, 0.93))
    fig.savefig(FIG_DIR / f"{name}.png")
    plt.close(fig)
    print(f"wrote outputs/figures/{name}.png")


# Figure 1 ---------------------------------------------------------------
def fig1_timeseries(data: pd.DataFrame) -> None:
    txx = data[data["indicator"] == "TXx"]
    fig, ax = grid("Figure 1. Summer maximum temperature (TXx) anomaly, 1950–2025",
                   f"Dots: June, July and August values; line: their yearly mean. Anomaly in °C "
                   f"from the {EARLY[0]}–{EARLY[1]} mean of the same month. Shaded: the two compared "
                   f"periods. Dashed line: {ROBUSTNESS_START}, before which ERA5-Land may be less consistent.")
    for c, a in ax.items():
        d = txx[txx["country"] == c]
        a.axvspan(EARLY[0] - 0.5, EARLY[1] + 0.5, color=C_EARLY, alpha=0.08, lw=0)
        a.axvspan(RECENT[0] - 0.5, RECENT[1] + 0.5, color=C_RECENT, alpha=0.08, lw=0)
        a.axvline(ROBUSTNESS_START, color=C_MUTED, ls="--", lw=0.8)
        a.axhline(0, color=C_MUTED, lw=0.8)
        a.scatter(d["year"], d["analysis_value"], s=6, color=C_MUTED, alpha=0.45, lw=0)
        yearly = d.groupby("year")["analysis_value"].mean()
        a.plot(yearly.index, yearly.values, color=C_INK, lw=1.4)
        a.set_title(NAMES[c], loc="left")
    for c in ("ESP", "GER"):
        ax[c].set_ylabel("TXx anomaly (°C)")
    ax["ESP"].text(np.mean(EARLY), 0.97, "early", transform=ax["ESP"].get_xaxis_transform(),
                   ha="center", va="top", color=C_EARLY, fontsize=8)
    ax["ESP"].text(np.mean(RECENT), 0.97, "recent", transform=ax["ESP"].get_xaxis_transform(),
                   ha="center", va="top", color=C_RECENT, fontsize=8)
    save(fig, "fig1_txx_timeseries")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    data = load_analysis_data()
    shift = pd.read_csv(OUT_DIR / "shift_shape.csv")
    exc = pd.read_csv(OUT_DIR / "exceedance.csv")
    fig1_timeseries(data)


if __name__ == "__main__":
    main()
