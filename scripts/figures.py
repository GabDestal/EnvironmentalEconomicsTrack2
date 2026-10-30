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


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    data = load_analysis_data()
    shift = pd.read_csv(OUT_DIR / "shift_shape.csv")
    exc = pd.read_csv(OUT_DIR / "exceedance.csv")


if __name__ == "__main__":
    main()
